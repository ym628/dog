# -*- coding: utf-8 -*-
import cv2
import time
import numpy as np
import mindspore_lite as mslite
import os


def sigmoid(x):
    """Sigmoid函数 - 修复数值范围问题"""
    # 先对输入进行归一化，防止数值过大
    x = np.clip(x, -20, 20)  # 限制在合理范围内
    return 1.0 / (1.0 + np.exp(-x))


def postprocess(
        feats,
        conf_thres: float = 0.1,
        num_classes: int = 80
):
    """后处理函数 - 调整以适应MindIR输出"""
    boxes = []
    scores = []
    labels = []
    strides = [8, 16, 32]
    anchors = [
        [[10, 13], [16, 30], [33, 23]],
        [[30, 61], [62, 45], [59, 119]],
        [[116, 90], [156, 198], [373, 326]]
    ]
    
    for i, stride in enumerate(strides):
        feat = feats[i]
        batch, num_anchors, h, w, channels = feat.shape
        
        curr_anchors = np.array(anchors[i], dtype=np.float32) / stride
        
        feat = feat[0]  # 取batch中的第一个
        
        for anchor_idx in range(num_anchors):
            a_feat = feat[anchor_idx]
            anchor = curr_anchors[anchor_idx]
            
            tx = a_feat[..., 0]
            ty = a_feat[..., 1]
            tw = a_feat[..., 2]
            th = a_feat[..., 3]
            obj_conf = sigmoid(a_feat[..., 4])
            cls_scores = sigmoid(a_feat[..., 5:5+num_classes])
            
            final_scores = cls_scores * obj_conf[..., None]
            max_scores = final_scores.max(axis=-1)
            max_labels = final_scores.argmax(axis=-1)
            
            mask = max_scores > conf_thres
            if not np.any(mask):
                continue
            
            valid_h, valid_w = np.where(mask)
            valid_scores = max_scores[valid_h, valid_w]
            valid_labels = max_labels[valid_h, valid_w]
            
            # 处理坐标预测
            tx_sig = sigmoid(tx[valid_h, valid_w])
            ty_sig = sigmoid(ty[valid_h, valid_w])
            
            # 限制tw/th的范围，防止exp溢出
            tw_clipped = np.clip(tw[valid_h, valid_w], -5, 5)
            th_clipped = np.clip(th[valid_h, valid_w], -5, 5)
            tw_exp = np.exp(tw_clipped)
            th_exp = np.exp(th_clipped)
            
            cx = (valid_w + tx_sig) * stride
            cy = (valid_h + ty_sig) * stride
            bw = anchor[0] * tw_exp * stride
            bh = anchor[1] * th_exp * stride
            
            x0 = cx - bw / 2
            y0 = cy - bh / 2
            box_width = bw
            box_height = bh
            
            for k in range(len(valid_h)):
                boxes.append([x0[k], y0[k], box_width[k], box_height[k]])
                scores.append(valid_scores[k])
                labels.append(valid_labels[k])
    
    if len(boxes) > 0:
        return (np.array(boxes, dtype=np.float32),
                np.array(scores, dtype=np.float32),
                np.array(labels, dtype=np.int32))
    else:
        return (np.array([], dtype=np.float32),
                np.array([], dtype=np.float32),
                np.array([], dtype=np.int32))


def non_max_suppression(
        boxes,
        scores,
        labels,
        conf_thres: float = 0.1,
        iou_thres: float = 0.45
):
    """非极大值抑制"""
    if len(boxes) == 0:
        return np.array([]), np.array([]), np.array([])

    boxes_list = boxes.tolist()
    scores_list = scores.tolist()

    indices = cv2.dnn.NMSBoxes(boxes_list, scores_list, conf_thres, iou_thres)
    if len(indices) == 0:
        return np.array([]), np.array([]), np.array([])

    indices = indices.flatten()
    return boxes[indices], scores[indices], labels[indices]


def main():
    # 模型路径
    model_path = '/home/HwHiAiUser/demo/weights/yolo.mindir'
    input_size = (640, 640)

    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        print(f"错误: 模型文件不存在: {model_path}")
        return

    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("错误: 无法打开摄像头")
        return

    # 设置摄像头分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    try:
        # 使用 MindSpore Lite 加载模型
        context = mslite.Context()
        context.target = ["Ascend"]
        context.ascend.device_id = 0
        
        model = mslite.Model()
        print(f"正在加载 MindSpore Lite 模型: {model_path}")
        model.build_from_file(model_path, mslite.ModelType.MINDIR, context)
        print(f"模型加载成功: {model_path}")
        
        # 获取输入输出
        inputs = model.get_inputs()
        print(f"输入形状: {inputs[0].shape}")
        
    except Exception as e:
        print(f"模型加载失败: {e}")
        cap.release()
        return

    print("开始实时检测... 按 'q' 退出, 's' 保存当前帧, 'd' 调试")
    print("只显示 'person' 检测结果")

    frame_count = 0
    fps_time = time.perf_counter()
    debug_mode = False
    person_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("错误: 无法获取帧")
            break

        # 计算FPS
        frame_count += 1
        current_time = time.perf_counter()
        
        if frame_count % 30 == 0:
            fps = 30 / (current_time - fps_time)
            print(f"FPS: {fps:.2f}")
            fps_time = current_time

        orig_h, orig_w = frame.shape[:2]

        # 预处理
        resized_img = cv2.resize(frame, input_size)
        input_img = resized_img[:, :, ::-1].transpose(2, 0, 1)
        input_img = np.expand_dims(input_img, axis=0)
        input_img = input_img.astype(np.float32) / 255.0
        input_img = np.ascontiguousarray(input_img)
        model.resize(inputs,[list(input_img.shape)])
        # 推理
        try:
            inputs[0].set_data_from_numpy(input_img)
            outputs = model.predict(inputs)
            output_data = [output.get_data_to_numpy() for output in outputs]
        except Exception as e:
            print(f"推理失败: {e}")
            continue

        # 使用特征图输出 (输出1-3)
        if len(output_data) >= 4:
            target_feats = output_data[1:4]  # 使用第1、2、3个输出
            
            # 调试信息
            if debug_mode:
                print(f"\n=== 调试信息 ===")
                print(f"输出数量: {len(output_data)}")
                for i, out in enumerate(output_data[1:4]):
                    print(f"特征图 {i+1}: 形状={out.shape}, 范围=[{out.min():.3f}, {out.max():.3f}], 均值={out.mean():.3f}")
            
            # 后处理
            boxes, scores, labels = postprocess(feats=target_feats, conf_thres=0.01)  # 降低阈值
            boxes, scores, labels = non_max_suppression(boxes, scores, labels, conf_thres=0.01, iou_thres=0.45)
            
            if debug_mode:
                print(f"检测到 {len(boxes)} 个框")
                if len(boxes) > 0:
                    print(f"标签分布: {np.bincount(labels)}")
                    
                    # 显示前几个检测结果
                    for i in range(min(3, len(boxes))):
                        label = labels[i]
                        score = scores[i]
                        class_name = "person" if label == 0 else f"class_{label}"
                        print(f"检测 {i}: {class_name}, 置信度={score:.3f}")
        else:
            boxes, scores, labels = np.array([]), np.array([]), np.array([])

        # 绘制检测结果
        scale_w = orig_w / input_size[0]
        scale_h = orig_h / input_size[1]
        
        person_count = 0  # 重置人数计数

        for box, score, label in zip(boxes, scores, labels):
            # 只显示标签为"person"（索引0）且置信率大于0.3的检测结果
            if label == 0 and score > 0.3:
                person_count += 1
                x0, y0, w, h = box.astype(np.int32)
                x0_scaled = int(x0 * scale_w)
                y0_scaled = int(y0 * scale_h)
                x1_scaled = int((x0 + w) * scale_w)
                y1_scaled = int((y0 + h) * scale_h)

                # 使用固定的颜色显示person（红色）
                cv2.rectangle(frame, (x0_scaled, y0_scaled), (x1_scaled, y1_scaled),
                              (0, 0, 255), 2, cv2.LINE_AA)
                label_text = f"Person {score:.2f}"
                cv2.putText(frame, label_text,
                            (x0_scaled, max(y0_scaled - 5, 0)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        
        # 显示FPS和人数统计
        fps = 1.0 / (time.perf_counter() - current_time)
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Persons: {person_count}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if debug_mode:
            cv2.putText(frame, "DEBUG MODE", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # 显示结果
        cv2.imshow('YOLOv5 Person Detection', frame)

        # 按键处理
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            timestamp = int(time.time())
            filename = f'capture_{timestamp}.jpg'
            cv2.imwrite(filename, frame)
            print(f"帧已保存: {filename}")
        elif key == ord('d'):
            debug_mode = not debug_mode
            print(f"调试模式 {'开启' if debug_mode else '关闭'}")

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("摄像头已释放")


if __name__ == '__main__':
    main()