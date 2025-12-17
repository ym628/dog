import numpy as np
import mindspore_lite as mslite
import mindspore
from mindspore import Tensor
from src.utils.cv_utils import nms, scale_coords, preprocess_image_yolov5
from src.utils import log


class YoloV5:
    def __init__(self, model_path):
        self.neth = 640
        self.netw = 640
        self.conf_threshold = 0.1
        dic = {0: 'left',
               1: 'right',
               2: 'stop',
               3: 'turnaround'}
        self.names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush']
        self.cfg = {
            'conf_thres': 0.6,
            'iou_thres': 0.5,
            'input_shape': [640, 640],
        }
        self.model_path = model_path

    def infer(self, in_queue, out_queue):
        
        context = mslite.Context()
        context.target = ["Ascend"]
        context.ascend.device_id = 0
        self.model = mslite.Model()
        log.info(f'yolov5 mslite model init...')
        print("self.model_path",self.model_path)
        self.model.build_from_file(self.model_path, mslite.ModelType.MINDIR, context)
        
        while True:
            while in_queue.empty():
                continue
            img_bgr = in_queue.get()
            img, scale_ratio, pad_size = preprocess_image_yolov5(img_bgr, self.cfg)
            
            # 扩展img的shape为(1,3,640,640)
            if len(img.shape) == 3:  # 如果是(3,640,640)
                img = np.expand_dims(img, axis=0)  # 变为(1,3,640,640)
            elif img.shape[0] != 1:  # 如果是(n,3,640,640)且n>1
                img = img[0:1]
            
            print(f"Expanded image shape: {img.shape}")
            
            # 模型推理
            inputs = self.model.get_inputs()
            self.model.resize(inputs, [list(img.shape)])
            inputs[0].set_data_from_numpy(img)
            
            outputs = self.model.predict(inputs)
            outputs = [output.get_data_to_numpy().copy() for output in outputs]
            output = outputs[0]
            print(f'output.shape:{output.shape}')

            # 转换为 MindSpore Tensor
            output = Tensor(output, mindspore.float32)
            
            # 非极大值抑制后处理 - 返回的是MindSpore Tensor列表
            boxout = nms(output, conf_thres=self.cfg["conf_thres"], iou_thres=self.cfg["iou_thres"])
            
            # ============ 注意：这里需要处理boxout可能为空的边界情况 ============
            if boxout is None or len(boxout) == 0:
                print("No NMS results")
                out_queue.put([])
                continue
            
            # 获取第一张图片的检测结果
            pred_result = boxout[0]
            
            # 检查是否有检测结果
            if pred_result is None or pred_result.shape[0] == 0:
                print("No detection results")
                out_queue.put([])
                continue
            
            try:
                # 将 MindSpore Tensor 
                pred_all = pred_result.asnumpy()
                print(f"Predicted boxes before scaling: {pred_all.shape}")
                
                # 检查数据格式
                if pred_all.shape[1] >= 6:
                    # 预测坐标转换
                    if pred_all[:, :4].shape[0] > 0:
                        try:
                            scale_coords(
                                self.cfg['input_shape'], 
                                pred_all[:, :4], 
                                img_bgr.shape, 
                                ratio_pad=(scale_ratio, pad_size)
                            )
                        except Exception as e:
                            print(f"Error in scale_coords: {e}")
                            # 如果坐标转换失败，使用原始坐标
                    
                    pred_boxes = []
                    for idx in range(pred_all.shape[0]):
                        confidence = float(pred_all[idx, 4])
                        if confidence < 0.05:
                            continue
                        
                        # 获取类别ID
                        if pred_all.shape[1] > 5:
                            class_id = int(pred_all[idx, 5])
                        else:
                            class_id = 0
                        
                        # 获取类别名称
                        if class_id < len(self.names):
                            obj_name = self.names[class_id]
                        else:
                            obj_name = f'class_{class_id}'
                        
                        # 如果只需要检测person，过滤其他类别
                        if obj_name != 'person':
                            continue
                        
                        x1 = int(pred_all[idx, 0])
                        y1 = int(pred_all[idx, 1])
                        x2 = int(pred_all[idx, 2])
                        y2 = int(pred_all[idx, 3])
                        
                        pred_boxes.append([x1, y1, x2, y2, obj_name, confidence])
                    
                    print(f"Detected {len(pred_boxes)} persons")
                    out_queue.put(pred_boxes)
                else:
                    print(f"Warning: Prediction has wrong shape: {pred_all.shape}")
                    out_queue.put([])
            except Exception as e:
                print(f"Error processing NMS results: {e}")
                out_queue.put([])