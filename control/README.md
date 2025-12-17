# 机械狗烧录代码

 代码部分

```
control	
  ├── esp32_code #机械狗esp32烧录代码
  │	 ├── dogee_ctrl_esp32.ino #esp32烧录代码
  │	 ├── ESP32_Servo.cpp #esp32的Arduino库
  │	 └── ESP32_Servo.h #esp32的Arduino库
  ├── stm32_code #机械狗stm32烧录代码
  │	 ├── QuadrupedF103（从控） #stm32F103从控烧录代码
  │	 ├── QuadrupedF405（主控） #stm32F405主控烧录代码
  └──README.md #
```

## stm32













## esp32
Arduino是一套便捷、灵活、容易上手的硬件开发平台，它包括多种型号的Arduino控制电路板和专用编程开发软件，能帮助用户快速的开发出智能硬件原型。
1. 进入[Arduino官网](https://www.arduino.cc/en/software)下载程序安装包“arduino-ide_version_Windows_64bit.exe”，并按照默认配置安装。
![image.png](https://raw.gitcode.com/user-images/assets/8737315/bc0d35a3-ffee-4391-8235-699ffba2f0a2/image.png 'image.png')
2. 双击打开软件，修改语言为中文。
![image.png](https://raw.gitcode.com/user-images/assets/8737315/4fb85b93-6884-4028-a133-856d35801cfc/image.png 'image.png')
2.选择“中文(简体)”
![image.png](https://raw.gitcode.com/user-images/assets/8737315/ebe38443-126d-4dca-8dd9-fc5586fab4fb/image.png 'image.png')
3. 安装ESP32开发板。

	a.在线安装
![image.png](https://raw.gitcode.com/user-images/assets/8737315/4f1e7c51-e4eb-438b-889e-1a660852587e/image.png 'image.png')
在“其他开发板管理器地址”中输入“https://www.arduino.cn/package_esp32_index.json”与“https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json”或单击
![image.png](https://raw.gitcode.com/user-images/assets/8737315/95a5ef08-5893-4639-9739-f246582a528a/image.png 'image.png')
图标在文本框中输入开发板管理器地址，单击确定保存
![image.png](https://raw.gitcode.com/user-images/assets/8737315/adfdea99-ce2b-4be3-8d39-2ced33d7398b/image.png 'image.png')
	b.离线安装
    
    离线安装ESP32开发板，单击链接下载Arduino的ESP32开发板安装包，下载完成后双击安装文件进行默认安装，安装完成后重启Arduino IDE。
![image.png](https://raw.gitcode.com/user-images/assets/8737315/e01fcaab-32be-4329-a9ff-875998672197/image.png 'image.png')

	***此步骤中安装ESP32组件，推荐使用离线安装的方式，用户也可以自行搜索在线安装的方法，但由于国内网络等问题，在线安装过程很可能会非常慢甚至安装失败。***

4.在“开发板”中选择ESP32开发板
![image.png](https://raw.gitcode.com/user-images/assets/8737315/5501fc2f-3fce-4b06-86c3-843bb5f1eb6b/image.png 'image.png')
***若没有出现COM串行端口，可能是由于电脑没有安装USB串口驱动，需自行下载并安装CH340驱动工具。***

5.获得ESP32开发板代码目录“dog\control\esp32_code”。

将dogee_control\esp32_code下的“ESP32_Servo.cpp”、“ESP32_Servo.h”,文件复制到Arduino库文件路径下，例如：
“C:\Users\10459\AppData\Local\Arduino15\packages\esp32\hardware\esp32\1.0.6\cores\esp32”。

6.烧录代码到ESP32开发板

在PC使用Arduino工具单击“文件>打开”按钮，选择“control\esp32_code\dogee_ctrl_esp32.ino”文件打开。
![image.png](https://raw.gitcode.com/user-images/assets/8737315/fb845674-2860-42c9-9965-d24cc2d6b28e/image.png 'image.png')

7.用USB数据线连接PC和ESP32开发板，单击“工具 > 端口”，选择新增的COM串行端口作为Arduino与ESP32开发板传输数据的通道
![image.png](https://raw.gitcode.com/user-images/assets/8737315/3e34a66d-96af-41dc-9066-63c3ca78082f/image.png 'image.png')
8.在Arduino工具中单击
![image.png](https://raw.gitcode.com/user-images/assets/8737315/2acbf6d5-5e08-4eda-ad3e-eb46b1a6380c/image.png 'image.png')按钮烧录控制代码至ESP32单片机   
开始编译项目
![image.png](https://raw.gitcode.com/user-images/assets/8737315/4ee38273-53cc-4872-80ef-44ce28979031/image.png 'image.png')
烧录回显
![image.png](https://raw.gitcode.com/user-images/assets/8737315/8ae84a63-b7a6-4391-b9af-250833b12954/image.png 'image.png')