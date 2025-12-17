MindSpore：https://www.mindspore.cn/  
MindSpore Lite：https://www.mindspore.cn/lite/
## 代码部分

本项目涉及机械狗控制底层代码，简单运动和复杂运动代码，各类工具以及多个推理模型，工程目录如下图所示：

```
demo
├── main.py	#demo运行总入口
├── src
│	 ├── actions #机械狗基础与复杂运动代码。
│	 ├── models #推理模型相关代码。
│	 ├── scenes #机械狗预设场景相关代码。
│	 └── utils #工具类python文件
├── weights #模型权重文件
│	 ├── hand_det.mindir #mindir格式手势模型权重
│	 ├── hand_det.om #om格式手势模型权重
│	 ├── yolo.mindir #mindir格式人体模型权重
│	 └── yolo.om #om格式人体模型权重
├── msliteyolo5.py	#摄像头进行人体推理
├── msliteyolo7.py	#摄像头进行手势推理
└──requirements.txt #demo样例所需依赖

```
## 环境部署
模型推理使用MindSpore Lite  ，需部署MindSpore Lite环境  
参考链接：https://www.mindspore.cn/lite/docs/zh-CN/r2.6.0/mindir/runtime_python.html
### 运行环境
```
MindSpore 2.6.0
CANN 8.1 RC 1
Python 3.9.2
```
查询开发板底层架构
```
uname -m
```
![c05ac328-06c8-4850-bf29-4b53abce30a4.png](https://raw.gitcode.com/user-images/assets/8737315/f9c589ca-02aa-4dd3-9213-e8f2cb6e7b9b/c05ac328-06c8-4850-bf29-4b53abce30a4.png 'c05ac328-06c8-4850-bf29-4b53abce30a4.png')
### 下载MindSpore Lite Python接口开发库
下载链接:https://www.mindspore.cn/lite/docs/zh-CN/r2.7.1/use/downloads.html#2-6-0 

操作系统根据上述命令进行查看，进行对应版本下载

![ff21f775-725a-4f5a-ba0d-3727cef3aba6.png](https://raw.gitcode.com/user-images/assets/8737315/f159d5e4-d23f-42a4-ac6f-986b9b3171df/ff21f775-725a-4f5a-ba0d-3727cef3aba6.png 'ff21f775-725a-4f5a-ba0d-3727cef3aba6.png')
### 安装MindSpore Lite Python接口开发库
```
pip install mindspore_lite-2.6.0-cp39-cp39-linux_aarch64.whl
```
![3da9f381407f694805f370f95147ec76.png](https://raw.gitcode.com/user-images/assets/8737315/1f5f60ff-b662-4e79-9ae7-df0ab56923df/3da9f381407f694805f370f95147ec76.png '3da9f381407f694805f370f95147ec76.png')
安装成功

### 下载MindSpore Lite开发库
![image.png](https://raw.gitcode.com/user-images/assets/8737315/2ea1416b-4094-4558-9788-81ecb449d16b/image.png 'image.png')

### 解压MindSpore Lite开发库
```
tar -zxvf mindspore-lite-2.6.0-linux-aarch64.tar.gz
```
![ef759ca1-33f6-4a6f-8492-6a5ab8a903ec.png](https://raw.gitcode.com/user-images/assets/8737315/911e38de-de04-49a5-a504-99e3ac93a75f/ef759ca1-33f6-4a6f-8492-6a5ab8a903ec.png 'ef759ca1-33f6-4a6f-8492-6a5ab8a903ec.png')
### 设置MindSpore Lite 根目录环境变量：
```
export LITE_HOME=[path to mindspore_lite_xxx]
export LD_LIBRARY_PATH=$LITE_HOME/runtime/lib:$LITE_HOME/tools/converter/lib:$LD_LIBRARY_PATH
export PATH=$LITE_HOME/tools/converter/converter:$LITE_HOME/tools/benchmark:$PATH
export Convert=$LITE_HOME/tools/converter/converter/converter_lite
```
注意：需要结合自身目录进行修改

### Convert(可选)
指导文档:https://www.mindspore.cn/lite/docs/zh-CN/r2.7.1/mindir/converter_tool.html

作用：模型提速，从MindIR（任何平台都能用）转换为mindspore专属的MindIR（针对昇腾有专属的优化）对环境进行优化

效果：启动推理速度更快
```
$Convert --fmk=MINDIR --modelFile=yolov7-tiny.mindir --outputFile=Converty7 --saveType=MINDIR --optimize=ascend_oriented
```
![a65ba35f-9063-4205-999e-2b38f2e31991.png](https://raw.gitcode.com/user-images/assets/8737315/94e12782-6cb9-4ee9-a5ec-72cd7771ce04/a65ba35f-9063-4205-999e-2b38f2e31991.png 'a65ba35f-9063-4205-999e-2b38f2e31991.png')



## 手动控制机械狗运动

执行以下命令，进入到开发板上机械狗的代码目录下。

```python
cd  /home/HwHiAiUser/E2ESample/ascend-devkit-master/src/E2E-Sample/dogee/demo
```

执行以下命令启动脚本，即可手动控制机械狗进行移动。

```python
python3 main.py
```

相对应的键盘控制表如下所示。

| 按键  | 机械狗动作 |
| :---- | ---------- |
| W     | 前进       |
| S     | 后退       |
| A     | 左转       |
| D     | 右转       |
| Space | 停止       |

## 机械狗锁定目标追踪

将机械狗放置在距离追踪目标人2-3m距离。

执行以下命令，进入到开发板上机械狗的代码目录下：

```python
cd  /home/HwHiAiUser/demo
```

执行以下命令启动脚本，等待机械狗初始化。

```python
python3 main.py --mode=tracking
```

初始化完成回显如下所示：
![屏幕截图 2025-12-17 114824.png](https://raw.gitcode.com/user-images/assets/8737315/894b753d-d528-4880-9fe3-6000808277a2/屏幕截图_2025-12-17_114824.png '屏幕截图 2025-12-17 114824.png')

在机械狗面前摆出“OK”的手势，等待开发者套件远程登录界面回显中出现**locked**，即表示已经锁定了追踪的目标，接下来就可以缓慢移动，机械狗就会跟随目标了。
![005d94a4-aea3-4d54-a5b8-a619e794f60c.png](https://raw.gitcode.com/user-images/assets/8737315/501835b0-8b24-44d1-b49f-f82c1300258a/005d94a4-aea3-4d54-a5b8-a619e794f60c.png '005d94a4-aea3-4d54-a5b8-a619e794f60c.png')

解除追踪锁定，可参见以下两种方式：

- 面对机械狗，手掌对向摄像头，五指张开，持续3s左右，开发者套件远程登录界面回显中出现**unlock**字样，即表示解除了锁定，机械狗会保持静止状态。
- 快速脱离机械狗的视线超过10s左右，机械狗会认为丢失目标，开发者套件远程登录界面回显中出现**unlock**字样，即表示解除了锁定，机械狗会保持静止状态。
![81c728b180ee251db1da66e523d89fb4.png](https://raw.gitcode.com/user-images/assets/8737315/630d631f-6b72-43ed-a724-90093c1eda80/81c728b180ee251db1da66e523d89fb4.png '81c728b180ee251db1da66e523d89fb4.png')