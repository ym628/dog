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