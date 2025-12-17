# 模型训练

mindyolo：[GitHub - mindspore-lab/mindyolo: A toolbox of yolo models and algorithms based on MindSpore](https://github.com/mindspore-lab/mindyolo/)



```
train
├── coco.yaml	#配置数据集及训练种类
├── export.py	#模型转换脚本
├── hyp.scratch.tiny.yaml	#设置超参数
├── predict.py	#推理脚本
├── train.py	#训练的启动代码
└──yolov7-tiny.yaml #配置训练参数
```

##  **简介**

使用MindYolo进行模型训练.

## **运行环境**

华为云model arts

MindSpore 2.5

昇腾910B4

硬盘：60G存储

## **安装依赖**

```shell
# 克隆 mindyolo 仓库
git clone https://github.com/mindspore-lab/mindyolo.git
cd mindyolo
 
# 安装依赖
pip install -r requirements.txt
 
# 安装 mindyolo 到当前环境
pip install -e .
```

```shell
pip install mindspore==2.5.0
```

## **配置文件**

本训练采用单卡训练，以下为配置文件

train.py是训练的启动代码

hyp.scratch.tiny.yaml是设置超参数

yolov7-tiny.yaml配置训练参数

coco.yaml配置数据集及训练种类，nc为数据集的种类，names为数据集的名称，这里因为我数据集里只有ok和palm手势所以我修改为：nc:2，names:['ok','palm']

数据集来源：[数据集-OpenDataLab](https://opendatalab.org.cn/sdf/Dataset/tree/main)

## **启动训练**

```
python train.py --config ./yolov7-tiny.yaml
```

## **模型测试**

predict.py是模型推理脚本

启动模型推理脚本

```
python predict.py --config ./yolov7-tiny.yaml --weight=./EMA_yolov7-299_12.ckpt --image_path ./yolo/images/000016.jpg
```

--config后面是yolov7的yaml文件

--weight 是训练后模型权重

--image_path 要识别的图片





