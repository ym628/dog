# 机械狗

## 外观结构

机械狗运动部分是由以下部分组成：

1. 四个具有2自由度的机械腿以及中间的主体部分实现的，机械腿的曲柄连杆结构保证了机械狗可以单独操作每一条腿的运动，每条腿上的两个关节由两个行星轮减速电机驱动，并放置在中间的主体部分。
2. 下位机由带有串口扩展板的两个STM32单片机开发板构成，分为主控F405和从控F103，位于机械狗身体内部。
3. 使用补充的3D连接固定件固定摄像头云台、开发板以及开发板电源
4. 摄像头云台连接一块ESP32下位机控制摄像头的移动，再通过USB扩展坞将所有的线连接到开发板上，再使用Wifi模块连接到开发板上。

**图1** 机械狗外观结构图
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001650180870.png)

## 功能与原理介绍

**图1** 功能原理图
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001663635202.png)

机械狗分为上位机即Atlas 200I DK A2开发者套件板，下位机即STM32和ESP32单片机，通过命令行以及手势语音等方式输入到机械狗上的各类传感器以及上位机上，在场景切换后进入到主函数，初始化各类硬件底层设备完成之后，就可以进入到各个场景对应的模块中进行信息拉取和推理进程了。以摄像头的为例，利用摄像头拉流到视频信息之后，输入到场景循环函数中，经过CV模型得到推理结果，再将后处理的结果回传到场景循环模块中，针对控制模块做动作下发，传递到STM32下位机上控制四足的运动，即可完成一个简单的流程。

## 控制与运动部分

机械狗的运动控制部分的实现原理图如[图1](https://www.hiascend.com/document/detail/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application Cases/mdadg/mdadg_0004.html#ZH-CN_TOPIC_0000001698579689__fig1081703063911)所示：

**图1** 机械狗运动控制原理图
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001663795214.png)

在上位机（开发者套件）上部署离线推理模型后，在上位机上根据推理结果生成对应的运动控制指令。指令下发到STM32单片机上，由串口中断函数来进行串口数据传输的接收。在上位机端和STM32使用相同的校验码的生成和校验方式，如果串口处接收到是上位机发出的指令，则会进入到对应的中断函数中进行运动状态的改变和操作。

在下位机（STM32）的初始化过程中：

1. 会开启多个任务序列，包括初始化电机零点位置、陀螺仪初始化、显示屏显示、LED灯显示、蜂鸣器初始化及串口发送数据初始化中断函数标记归位等操作。
2. 主进程在完整这些操作之后，进入获取控制端以及四足行动的部分，在收取到上位机发出的指令后，下位机进行解析，获取机器狗的姿态全局变量参数以及运动的两个方向的线速度和角速度。
3. 进入到机械狗的运动解析部分进行运算，解析接下来的运动需中每一个机械腿的运动位置，以及八个电机需要转到的目标位置，并下发指令到从控的STM32上，通过串口下发到电机处。其中的电机使用PID来编码，在整个姿态变化和运动的过程中，通过PID控制电机的目标位置和实际运动位置误差以及自我纠正误差。
4. 同时，为了防止运动过程中机械狗摔倒，加入了陀螺仪的运算，且可以在显示屏上显示实际数据。MPU6050陀螺仪会计算平衡环的数值大小用来修正不同方向上的非水平位置变化，然后加入到机械腿的运动控制中。得到了控制机械腿的目标位置后，可以通过机械腿路径规划算法实现实时计算机械腿机械腿的运动位置，使机械狗能够稳步前进以及完成其他动作。

**图2** 运动控制时序图1
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001711731005.png)

**图3** 运动控制时序图2
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001663811150.png)

## 锁定追踪部分

机械狗的锁定追踪部分的时序图如[图1](https://www.hiascend.com/document/detail/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application Cases/mdadg/mdadg_0006.html#ZH-CN_TOPIC_0000001698579697__fig167949134018)、[图2](https://www.hiascend.com/document/detail/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application Cases/mdadg/mdadg_0006.html#ZH-CN_TOPIC_0000001698579697__fig216418211412)和[图3](https://www.hiascend.com/document/detail/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application Cases/mdadg/mdadg_0006.html#ZH-CN_TOPIC_0000001698579697__fig223613525410)所示：

**图1** 机械狗锁定追踪时序图1
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001716066033.png)

**图2** 机械狗锁定追踪时序图2
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001668106754.png)

**图3** 机械狗锁定追踪时序图3
![img](https://www.hiascend.com/doc_center/source/zh/Atlas200IDKA2DeveloperKit/23.0.RC2/Application%20Cases/mdadg/figure/zh-cn_image_0000001716147201.png)

1. 在启动主程序后，首先进行摄像头和共享内存的初始化，拉流后在运动控制器端初始化，获取STM32和ESP32的端口信息。
2. 其中，外设的连接端口号ttyUSB*中具体的号码是由拔插的先后顺序决定的，所以需要提前查询端口信息并返回到主程序中。而后在追踪任务的进程中初始化，再开启两个手势识别和人体检测的模型进程，分别进行初始化，然后在控制端下位机设置舵机的角度，调整到方便机械狗追踪的角度，将识别锁定追踪目标的状态初始化为解锁，锁定计数归零。
3. 在拉流分发的进程中开启循环获取frame并放入共享内存中，然后再启动循环并开始并行的手势识别和人体识别的推理进程。此处使用两个消息队列来防止手势识别和人体识别出现异帧不同步的情况，将两个过程同步之后返回两个bboxes，分别是手势和人体的识别框存储数据，再利用如下公式来判断锁定的目标框：
   1. 在出现比值大于0.9的帧时，计数器值加1，在连续五帧都超过这个比值后，将锁定目标的FLAG置为True，然后设置舵机的信息，进行目标的锁定追踪；若在已经锁定目标的状态下就需要锁定到该框并且使用卡尔曼滤波的方式进行目标框的匹配，进而推算出要追随的目标，即使在有多人存在的场景仍然可以准确追踪到目标。
   2. 在超过20帧没有识别到目标之后以及出现解锁的手势超过5帧之后就会将机械狗的下位机中的运动FLAG设定为停止，然后上位机上的解锁标志回归为解锁，并且下发动作，然后等待下一个锁定的手势出现，继续追踪新的目标。

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