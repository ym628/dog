# -*- coding: utf-8 -*-
import cv2
import time
import random
import numpy as np
from numpy import ndarray
from typing import List, Tuple
import mindspore_lite as mslite

# 模型输入尺寸配置
MODEL_INPUT_SIZE = (640, 640)  # 640×640

CLASS_COLORS = [[random.randint(0, 255) for _ in range(3)] for _ in range(80)]
CLASS_NAMES = ('ok', 'palm')

def sigmoid(x: ndarray) -> ndarray:
    return 1.0 / (1.0 + np.exp(-x))

def xywh2xyxy(x: ndarray) -> ndarray:
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2 
    return y

def non_max_suppression(
        prediction: ndarray,
        conf_thres: float = 0.25,
        iou_thres: float = 0.45,
        classes: List[int] = None,
        agnostic: bool = False) -> List[ndarray]:
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
        
        detections = np.concatenate((box, conf.max(1, keepdims=True), conf.argmax(1, keepdims=True).astype(np.float32)), 1)
        
        detections = detections[detections[:, 4].argsort()[::-1]]
        
        keep = []
        while detections.shape[0]:
            large_overlap = _bbox_iou(detections[0, :4], detections[:, :4]) > iou_thres
            label_match = detections[0, -1] == detections[:, -1]
            
            if agnostic:
                overlap = large_overlap
            else:
                overlap = large_overlap & label_match
            
            keep.append(detections[0])
            
            detections = detections[~overlap]
        
        if keep:
            output[xi] = np.stack(keep)
    
    return output

def _bbox_iou(box1: ndarray, box2: ndarray) -> ndarray:
    inter_x1 = np.maximum(box1[0], box2[:, 0])
    inter_y1 = np.maximum(box1[1], box2[:, 1])
    inter_x2 = np.minimum(box1[2], box2[:, 2])
    inter_y2 = np.minimum(box1[3], box2[:, 3])
    
    inter_area = np.maximum(inter_x2 - inter_x1, 0) * np.maximum(inter_y2 - inter_y1, 0)
    
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[:, 2] - box2[:, 0]) * (box2[:, 3] - box2[:, 1])
    
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / (union_area + 1e-7)

def scale_coords(img_shape: Tuple[int, int], coords: ndarray, orig_shape: Tuple[int, int]) -> ndarray:
    gain = min(img_shape[0] / orig_shape[0], img_shape[1] / orig_shape[1]) 
    pad = (img_shape[1] - orig_shape[1] * gain) / 2, (img_shape[0] - orig_shape[0] * gain) / 2  
    
    coords[:, [0, 2]] -= pad[0] 
    coords[:, [1, 3]] -= pad[1] 
    coords[:, :4] /= gain  
    
    coords[:, [0, 2]] = coords[:, [0, 2]].clip(0, orig_shape[1])  
    coords[:, [1, 3]] = coords[:, [1, 3]].clip(0, orig_shape[0])  
    
    return coords
    
def postprocess_yolov7(
        outputs: List[ndarray],
        conf_thres: float = 0.25,
        iou_thres: float = 0.45,
        img_size: int = 320) -> Tuple[ndarray, ndarray, ndarray]:

    pred = outputs[0]  # shape: (1, 25200, 7)
    
    detections = non_max_suppression(pred, conf_thres, iou_thres)
    
    boxes_list = []
    scores_list = []
    labels_list = []
    
    for det in detections:
        if len(det) > 0:
            for *xyxy, conf, cls in det:
                boxes_list.append([xyxy[0], xyxy[1], xyxy[2] - xyxy[0], xyxy[3] - xyxy[1]])
                scores_list.append(conf)
                labels_list.append(int(cls))
    
    if boxes_list:
        boxes_pro = np.array(boxes_list, dtype=np.float32)
        scores_pro = np.array(scores_list, dtype=np.float32)
        labels_pro = np.array(labels_list, dtype=np.int32)
    else:
        boxes_pro = np.zeros((0, 4), dtype=np.float32)
        scores_pro = np.zeros((0,), dtype=np.float32)
        labels_pro = np.zeros((0,), dtype=np.int32)
    
    return boxes_pro, scores_pro, labels_pro

def preprocess_frame_fast(frame, target_size=320):
    """快速预处理摄像头帧 - 直接缩放，不保持宽高比"""
    # 直接缩放图像到目标尺寸
    resized = cv2.resize(frame, (target_size, target_size))
    
    # 转换为模型输入格式
    img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    img = img.transpose(2, 0, 1)  
    img = np.ascontiguousarray(img[np.newaxis], dtype=np.float32) / 255.0 
    
    return img

def init_mslite_model(model_path):
    """初始化MindSpore Lite模型"""
    # 创建上下文
    context = mslite.Context()
    context.target = ["Ascend"]
    
    # 创建模型
    model = mslite.Model()
    
    # 构建模型
    model.build_from_file(model_path, mslite.ModelType.MINDIR, context)
    
    # 获取输入输出信息
    inputs = model.get_inputs()
    outputs = model.get_outputs()
    
    print(f"Model loaded successfully")
    print(f"Inputs: {len(inputs)}")
    for i, inp in enumerate(inputs):
        print(f"  Input {i}: shape={inp.shape}, dtype={inp.dtype}")
    print(f"Outputs: {len(outputs)}")
    for i, out in enumerate(outputs):
        print(f"  Output {i}: shape={out.shape}, dtype={out.dtype}")
    
    return model

def infer_mslite(model, img):
    """使用MindSpore Lite进行推理"""
    # 获取模型输入
    inputs = model.get_inputs()
    
    # 设置输入数据
    inputs[0].set_data_from_numpy(img)
    
    # 执行推理
    outputs = model.predict(inputs)
    
    # 将输出转换为numpy数组
    output_numpy = [output.get_data_to_numpy().copy() for output in outputs]
    
    return output_numpy

def main():
    model_path = '/home/HwHiAiUser/demo/weights/hand_det.mindir'  # 修改为.mindir模型文件
    
    # 初始化MindSpore Lite模型
    print("Initializing MindSpore Lite model...")
    model = init_mslite_model(model_path)
    
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 0 表示默认摄像头
    
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    # 降低摄像头分辨率以提高帧率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 60)  # 设置帧率
    
    # 减少预热次数 - 使用正确的输入尺寸
    print("Warming up...")
    for i in range(5):
        tmp = np.random.randn(1, 3, MODEL_INPUT_SIZE[0], MODEL_INPUT_SIZE[1]).astype(np.float32)
        print(f"Warmup input shape: {tmp.shape}, size: {tmp.nbytes} bytes")
        infer_mslite(model, tmp)
    
    print("Starting real-time inference... Press 'q' to quit")
    
    # 帧率计算变量
    frame_count = 0
    fps = 0
    start_time = time.time()
    
    # 跳过帧计数器 - 每N帧进行一次推理
    skip_frames = 1  # 每2帧推理一次
    frame_counter = 0
    
    # 缓存上一帧的检测结果
    last_boxes = np.zeros((0, 4), dtype=np.float32)
    last_scores = np.zeros((0,), dtype=np.float32)
    last_labels = np.zeros((0,), dtype=np.int32)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame from camera")
            break
        
        frame_counter += 1
        
        # 只在特定帧上进行推理
        if frame_counter % (skip_frames + 1) == 0:
            # 快速预处理 - 使用MODEL_INPUT_SIZE
            img = preprocess_frame_fast(frame, target_size=MODEL_INPUT_SIZE[0])
            
            # 验证输入大小
            expected_size = 1 * 3 * MODEL_INPUT_SIZE[0] * MODEL_INPUT_SIZE[1] * 4
            if img.nbytes != expected_size:
                print(f"Warning: Input size mismatch! Expected: {expected_size}, Actual: {img.nbytes}")
                continue
            
            # 推理
            inference_start = time.time()
            outputs = infer_mslite(model, img)
            inference_time = time.time() - inference_start
            
            # 后处理
            boxes, scores, labels = postprocess_yolov7(outputs)
            
            # 缩放坐标回原始图像尺寸
            if len(boxes) > 0:
                boxes_xyxy = np.copy(boxes)
                boxes_xyxy[:, 2] = boxes_xyxy[:, 0] + boxes_xyxy[:, 2]  
                boxes_xyxy[:, 3] = boxes_xyxy[:, 1] + boxes_xyxy[:, 3]  
                
                # 缩放坐标 - 使用MODEL_INPUT_SIZE
                h, w = frame.shape[:2]
                boxes_xyxy[:, [0, 2]] *= w / MODEL_INPUT_SIZE[0]  # x坐标缩放
                boxes_xyxy[:, [1, 3]] *= h / MODEL_INPUT_SIZE[1]  # y坐标缩放
                
                boxes[:, 0] = boxes_xyxy[:, 0]
                boxes[:, 1] = boxes_xyxy[:, 1]
                boxes[:, 2] = boxes_xyxy[:, 2] - boxes_xyxy[:, 0]
                boxes[:, 3] = boxes_xyxy[:, 3] - boxes_xyxy[:, 1]
            
            # 更新缓存结果
            last_boxes = boxes
            last_scores = scores
            last_labels = labels
        else:
            # 使用缓存的检测结果
            boxes = last_boxes
            scores = last_scores
            labels = last_labels
            inference_time = 0  # 不计算推理时间
        
        # 绘制检测结果
        display_frame = frame.copy()
        for box, score, label in zip(boxes, scores, labels):
            if score > 0.25:  
                x1, y1, w, h = box.round().astype(np.int32).tolist()
                x2, y2 = x1 + w, y1 + h
                
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), CLASS_COLORS[label], 2, cv2.LINE_AA)
                
                label_text = f'{CLASS_NAMES[label]} {score:.2f}'
                label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(display_frame, (x1, y1 - label_size[1] - 5), (x1 + label_size[0], y1), CLASS_COLORS[label], -1)
                cv2.putText(display_frame, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        
        # 计算FPS
        frame_count += 1
        if frame_count % 10 == 0:
            end_time = time.time()
            fps = 10 / (end_time - start_time)
            start_time = end_time
        
        # 在画面上显示信息
        cv2.putText(display_frame, f'FPS: {fps:.1f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if inference_time > 0:
            cv2.putText(display_frame, f'Inference: {inference_time*1000:.1f}ms', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f'Detections: {len(boxes)}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f'Skip: {skip_frames}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f'Input: {MODEL_INPUT_SIZE[0]}x{MODEL_INPUT_SIZE[1]}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示结果
        cv2.imshow('YOLOv7 Real-time Detection', display_frame)
        
        # 按键处理
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # 按q退出
            break
        elif key == ord('+'):  # 按+减少跳帧
            skip_frames = max(0, skip_frames - 1)
        elif key == ord('-'):  # 按-增加跳帧
            skip_frames = min(10, skip_frames + 1)
        elif key == ord('r'):  # 按r重置跳帧
            skip_frames = 1
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("Real-time detection finished")

if __name__ == '__main__':
    main()