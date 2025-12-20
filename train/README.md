<span style="font-size:20px;">
本文档详细介绍了如何使用 MindYolo 框架训练手势识别模型，并直接下载人体模型，最终需将两者部署到昇腾开发板进行推理。</span>

# YOLOv7手势模型训练指南
[mindyolo](https://github.com/mindspore-lab/mindyolo/)：基于 MindSpore 的 YOLO 算法工具箱

[昇思大模型平台](https://xihe.mindspore.cn/)：提供在线训练与开发环境


## 训练代码结构

```
train
├── coco.yaml	#数据集配置：类别定义与数据路径
├── export.py	#模型格式转换脚本（ckpt → MindIR）
├── hyp.scratch.tiny.yaml	#超参数配置文件（学习率、优化器等）
├── mslite_predict.py	#MindIR 格式模型推理脚本
├── predict.py	#ckpt 格式模型推理脚本
├── train.py	#模型训练主程序
├── yolov7-tiny.yaml #YOLOv7-tiny 网络结构与训练参数配置
└── README.md #描述文件
```


## **训练环境配置**

计算资源: 昇思大模型平台

AI 处理器:昇腾910B

运行内存:192GB

存储空间:60G存储

框架版本:MindSpore 2.5

## **依赖安装步骤**
1.克隆 MindYolo 仓库并安装到当前环境
```shell
# 克隆 mindyolo 仓库
git clone https://github.com/mindspore-lab/mindyolo.git
cd mindyolo
 
# 安装依赖
pip install -r requirements.txt
 
# 安装 mindyolo 到当前环境
pip install -e .
```
2.安装 MindSpore 框架
```shell
pip install mindspore==2.5.0
```

## **配置文件详解**

### 数据集配置 (coco.yaml)
根据手势识别任务需求，修改以下参数：
```yaml
nc: 2                          # 类别数量（两种手势）
names: ['ok', 'palm']         # 类别名称列表
```
### 训练配置 (yolov7-tiny.yaml)
- 单卡训练配置

- 批次大小设置

- 训练轮数设定

- 优化器选择
### 超参数配置 (hyp.scratch.tiny.yaml)
- 学习率调度策略

- 权重衰减系数

- 数据增强参数

- 损失函数权重
## 模型训练流程


### **启动训练**
执行以下命令开始模型训练：
```
python train.py --config ./yolov7-tiny.yaml
```
![066d904eb9c5fd5b4332fd40a5bb026c.png](https://raw.gitcode.com/user-images/assets/8737315/5379c432-6b54-4e87-a991-e1bddb80da62/066d904eb9c5fd5b4332fd40a5bb026c.png '066d904eb9c5fd5b4332fd40a5bb026c.png')
训练成功提示：终端将显示训练进度、损失值变化和评估指标。

**训练监控**
- 实时显示训练损失曲线

- 定期输出模型评估结果

- 自动保存最佳模型权重

### **模型验证与测试**
1.使用 ckpt 权重进行推理

```python
python predict.py --config ./yolov7-tiny.yaml --weight=./EMA_yolov7-299_12.ckpt --image_path ./yolo/images/000016.jpg
```
**参数说明：**

--config: YOLOv7 配置文件路径

--weight: 训练得到的模型权重文件

--image_path : 测试图片路径
![34e04c0a2a566c0ae466171f87f48bee.jpg](https://raw.gitcode.com/user-images/assets/8737315/c9b0917a-2e6b-4a11-857c-c65063085c64/34e04c0a2a566c0ae466171f87f48bee.jpg '34e04c0a2a566c0ae466171f87f48bee.jpg')
推理完成，模型可用

2.模型格式转换（ckpt → MindIR）

将训练得到的 ckpt 模型转换为 MindSpore Lite 可用的 MindIR 格式：
```python
python ./export.py --config ./yolov7-tiny.yaml --weight EMA_yolov7-tiny-50_1250.ckpt --file_format MINDIR --device_target Ascend
```
![092de955-bb3a-4726-a168-43627f1f2050.png](https://raw.gitcode.com/user-images/assets/8737315/aa2f2574-2d3a-4d67-9ab3-de531895c5fb/092de955-bb3a-4726-a168-43627f1f2050.png '092de955-bb3a-4726-a168-43627f1f2050.png')
转换成功提示：生成 yolov7-tiny.mindir 模型文件。


3.MindIR 模型推理测试

验证转换后的 MindIR 模型在目标设备上的推理性能：
```python
python ./mslite_predict.py --mindir_path yolov7-tiny.mindir --config ./yolov7-tiny.yaml --image_path ./yolo/images/images/000005.jpg
```
![image.png](https://raw.gitcode.com/user-images/assets/8737315/8f0be699-1705-405a-bd2d-3279fc13e523/image.png 'image.png')
模型推理测试正常
## 数据集准备

本项目使用的训练数据集来自：[数据集-OpenDataLab](https://opendatalab.org.cn/sdf/Dataset/tree/main)
### 数据预处理
1. 下载并解压数据集

3. 转换为 COCO 标注格式

5. 划分训练集与验证集

7. 生成数据索引文件

## 训练效果评估
### 性能指标
1. 模型推理速度（FPS）

3. 手势识别准确率

5. 模型文件大小

7. 内存占用情况

# YOLOv5预训练模型下载指南
[MindSporeYolo](https://github.com/mindspore-lab/mindyolo/tree/master/deploy)：提供开箱即用的 MindIR 格式预训练目标检测模型（支持 YOLOv5/YOLOv8 等主流架构），支持免转换直接部署至昇腾 AI 处理器（Ascend 310/910）与支持 MindSpore Lite 的移动/边缘设备。

![ee4e72e4f062673e9a2d231ca1b20cd1.jpeg](https://raw.gitcode.com/user-images/assets/8737315/99402944-fca8-4d53-9ad6-fc46062993f1/ee4e72e4f062673e9a2d231ca1b20cd1.jpeg 'ee4e72e4f062673e9a2d231ca1b20cd1.jpeg')