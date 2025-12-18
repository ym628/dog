# 模型训练

mindyolo：[GitHub - mindspore-lab/mindyolo: A toolbox of yolo models and algorithms based on MindSpore](https://github.com/mindspore-lab/mindyolo/)

昇思大模型平台[](https://xihe.mindspore.cn/)：https://xihe.mindspore.cn/



```
train
├── coco.yaml	#配置数据集及训练种类
├── export.py	#模型转换脚本
├── hyp.scratch.tiny.yaml	#设置超参数
├── mslite_predict.py	#MindIR模型推理脚本
├── predict.py	#ckpt模型推理脚本
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
![066d904eb9c5fd5b4332fd40a5bb026c.png](https://raw.gitcode.com/user-images/assets/8737315/5379c432-6b54-4e87-a991-e1bddb80da62/066d904eb9c5fd5b4332fd40a5bb026c.png '066d904eb9c5fd5b4332fd40a5bb026c.png')
训练成功


## **模型测试**

predict.py是模型推理脚本

启动模型推理脚本

```
python predict.py --config ./yolov7-tiny.yaml --weight=./EMA_yolov7-299_12.ckpt --image_path ./yolo/images/000016.jpg
```

--config后面是yolov7的yaml文件

--weight 是训练后模型权重

--image_path 要识别的图片
![34e04c0a2a566c0ae466171f87f48bee.jpg](https://raw.gitcode.com/user-images/assets/8737315/c9b0917a-2e6b-4a11-857c-c65063085c64/34e04c0a2a566c0ae466171f87f48bee.jpg '34e04c0a2a566c0ae466171f87f48bee.jpg')
推理完成
## ckpt转MindIR
将上文得到的ckpt模型转化为MindIR格式
```
python ./export.py --config ./yolov7-tiny.yaml --weight EMA_yolov7-tiny-50_1250.ckpt --file_format MINDIR --device_target Ascend
```
![092de955-bb3a-4726-a168-43627f1f2050.png](https://raw.gitcode.com/user-images/assets/8737315/aa2f2574-2d3a-4d67-9ab3-de531895c5fb/092de955-bb3a-4726-a168-43627f1f2050.png '092de955-bb3a-4726-a168-43627f1f2050.png')
转换完成
## MindIR模型测试
```
python ./mslite_predict.py --mindir_path yolov7-tiny.mindir --config ./yolov7-tiny.yaml --image_path ./yolo/images/images/000005.jpg
```
![image.png](https://raw.gitcode.com/user-images/assets/8737315/8f0be699-1705-405a-bd2d-3279fc13e523/image.png 'image.png')
模型正常可用







