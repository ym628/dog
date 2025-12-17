# -*- coding: utf-8 -*-
import cv2
import numpy as np
import mindspore_lite as mslite

def xywh2xyxy(x):
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2 
    return y

def non_max_suppression_yolov7(prediction, conf_thres=0.25, iou_thres=0.45):
    box = prediction[..., :4]  
    conf = prediction[..., 4:5] 
    cls = prediction[..., 5:]
    
    scores = conf * cls
    box = xywh2xyxy(box)
    
    output = [np.zeros((0, 6))] * prediction.shape[0]
    
    for xi, x in enumerate(prediction):  
        x = x[scores[xi].max(1) > conf_thres]
        
        if not x.shape[0]:
            continue
        
        conf = x[:, 4:5] * x[:, 5:]
        box = xywh2xyxy(x[:, :4])
        
        detections = np.concatenate((box, conf.max(1, keepdims=True), 
                                   conf.argmax(1, keepdims=True).astype(np.float32)), 1)
        detections = detections[detections[:, 4].argsort()[::-1]]
        
        keep = []
        while detections.shape[0]:
            large_overlap = _bbox_iou(detections[0, :4], detections[:, :4]) > iou_thres
            label_match = detections[0, -1] == detections[:, -1]
            overlap = large_overlap & label_match
            
            keep.append(detections[0])
            detections = detections[~overlap]
        
        if keep:
            output[xi] = np.stack(keep)
    
    return output

def _bbox_iou(box1, box2):
    inter_x1 = np.maximum(box1[0], box2[:, 0])
    inter_y1 = np.maximum(box1[1], box2[:, 1])
    inter_x2 = np.minimum(box1[2], box2[:, 2])
    inter_y2 = np.minimum(box1[3], box2[:, 3])
    
    inter_area = np.maximum(inter_x2 - inter_x1, 0) * np.maximum(inter_y2 - inter_y1, 0)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[:, 2] - box2[:, 0]) * (box2[:, 3] - box2[:, 1])
    
    union_area = box1_area + box2_area - inter_area
    return inter_area / (union_area + 1e-7)

class YoloV7:
    def __init__(self, model_path):
        self.model = None
        self.model_path = model_path
        self.input_size = 640  # Keep original input size
        self.class_names = ('ok', 'palm')
        #self._init_mslite_model(model_path)
    
    def _init_mslite_model(self, model_path):
        """Initialize MindSpore Lite model"""
        # Create context

        
        # Get input and output information
        inputs = self.model.get_inputs()
        outputs = self.model.get_outputs()
        
        print(f"MindSpore Lite model loaded successfully")
        print(f"Inputs: {len(inputs)}")
        for i, inp in enumerate(inputs):
            print(f"  Input {i}: shape={inp.shape}, dtype={inp.dtype}")
        print(f"Outputs: {len(outputs)}")
        for i, out in enumerate(outputs):
            print(f"  Output {i}: shape={out.shape}, dtype={out.dtype}")

    def infer_mslite(self, img):
        """Inference using MindSpore Lite"""
        # Get model inputs
        inputs = self.model.get_inputs()
        
        # Set input data
        inputs[0].set_data_from_numpy(img)
        
        # Perform inference
        outputs = self.model.predict(inputs)
        #print("outputs",outputs)
        
        # Convert outputs to numpy array
        output_numpy = [output.get_data_to_numpy().copy() for output in outputs]
        
        return output_numpy

    def infer(self, in_queue, out_queue):
        """Main inference loop"""
        context = mslite.Context()
        context.target = ["Ascend"]
        
        # Create model
        self.model = mslite.Model()
        
        # Build model
        self.model.build_from_file(self.model_path, mslite.ModelType.MINDIR, context)
        while True:
            while in_queue.empty():
                continue
            frame = in_queue.get()
            
            # Preprocessing - keep original logic unchanged
            resized = cv2.resize(frame, (self.input_size, self.input_size))
            img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            img = img.transpose(2, 0, 1)  
            img = np.ascontiguousarray(img[np.newaxis], dtype=np.float32) / 255.0

            # Use MindSpore Lite for inference
            out = self.infer_mslite(img)
            
            # Postprocessing - keep original logic unchanged
            pred = out[0]
            detections = non_max_suppression_yolov7(pred, conf_thres=0.25, iou_thres=0.45)
            
            send_item = []
            for det in detections:
                if len(det) > 0:
                    for *xyxy, conf, cls in det:
                        # Convert coordinates to original image size
                        x1 = int(xyxy[0] * frame.shape[1] / self.input_size)
                        y1 = int(xyxy[1] * frame.shape[0] / self.input_size)
                        x2 = int(xyxy[2] * frame.shape[1] / self.input_size)
                        y2 = int(xyxy[3] * frame.shape[0] / self.input_size)
                        
                        cls_id = int(cls)
                        confidence = float(conf)
                        
                        send_item.append([x1, y1, x2, y2, cls_id, confidence])
            
            out_queue.put(send_item)