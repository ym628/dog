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
1. 请用户进入[官方网站](https://www.keil.com/demo/eval/arm.htm)完成信息注册，单击如图1所示图标，下载注册机软件。

图1 获取软件
![f0c828ec8c51fb9952eed6083fa1f9a5.png](https://raw.gitcode.com/user-images/assets/8737315/b74e02e8-7838-42c4-b690-bf59e34af75f/f0c828ec8c51fb9952eed6083fa1f9a5.png 'f0c828ec8c51fb9952eed6083fa1f9a5.png')

2. 按照默认配置通过注册机安装Keil uVision5软件及工具包。

3. 打开Keil uVision5软件，单击工具栏![image.png](https://raw.gitcode.com/user-images/assets/8737315/84c71398-4bfc-4aa8-a569-dd13f5ce99d2/image.png 'image.png')按钮，进入包管理工具。

图2 包管理工具界面
![image.png](https://raw.gitcode.com/user-images/assets/8737315/f10605e2-ec09-4d39-b6ea-e9a5c1adc1ed/image.png 'image.png')

4. 在搜索框中搜索STM32F1 Series与STM32F4 Series并安装所有包。

图3 搜索包

![image.png](https://raw.gitcode.com/user-images/assets/8737315/6bb372de-a1ef-4a55-81c1-69e928ead51e/image.png 'image.png')

5. 左键单击待下载的包，单击右侧工具框中的“Install”按钮安装。

图4 安装包
![image.png](https://raw.gitcode.com/user-images/assets/8737315/fcbaab2a-f444-4135-bf03-58e486d6c759/image.png 'image.png')

6. 在PC使用Keil uVision5选择工具栏“File > Open”，打开文件“control\stm32_code\QuadrupedF405\USER”目录下的“QuadrupedF405.uvprojx”项目文件，即可进入到对应的界面，如图6所示。

图5 打开文件

![image.png](https://raw.gitcode.com/user-images/assets/8737315/9954726e-bf76-4e8e-a7da-122ae998366c/image.png 'image.png')

图6界面图
![image.png](https://raw.gitcode.com/user-images/assets/8737315/f94899a8-8769-4142-a601-14388fde5921/image.png 'image.png')


<span style="color:#e60000;">说明:</span>

出现缺少头文件提示时，选择工具栏“Project > Options for Target ...”，请选择C/C++，为Project添加头文件的include path路径（路径不能出现中文字符）

![image.png](https://raw.gitcode.com/user-images/assets/8737315/fb594fe2-4df0-4302-b500-8c132df9f0b2/image.png 'image.png')

出现未识别include提示需要修改LanguageC从C90改为C99。

![image.png](https://raw.gitcode.com/user-images/assets/8737315/337898fd-06c1-4740-a5df-96a8d87b061c/image.png 'image.png')

7. 当前Keil uVision5软件已不提供Version5的编译器，需用户自行查找并安装。

图7 编译器丢失

![image.png](https://raw.gitcode.com/user-images/assets/8737315/987ecfd4-5ec7-43c1-9fef-d7e0b5663b87/image.png 'image.png')

8. 烧录STM32

图8 405主控板
![image.png](https://raw.gitcode.com/user-images/assets/8737315/e6cb58cb-dfee-4618-b672-5f03c7809e96/image.png 'image.png')    
    a. 由于STLINK的USB端串口位置固定，与STM32无法一一对应，所以需要使用杜邦线连接STLINK的USB端的串口，使其能够与开发板的串口对应，STM32串口位置如图9所示，STLINK的USB端串口位置如图10所示。
    
图9 STM32串口引脚
![image.png](https://raw.gitcode.com/user-images/assets/8737315/b63ae1c2-7ff4-4b67-b4ac-ee30b1ed858e/image.png 'image.png')
图10 STLINK的USB端串口位置

![image.png](https://raw.gitcode.com/user-images/assets/8737315/3b3074a1-f417-40d9-8a5a-ff94c0daff0e/image.png 'image.png')
    
   b. STLINK线的SWCLK串口与STM32开发板的A14连接，STLINK线的SWDIO串口与STM32开发板的A13连接，电源3.3V对应3.3V，GND串口对应GND
   
9. 在keil客户端准备完成后，单击![image.png](https://raw.gitcode.com/user-images/assets/8737315/99367dc0-401b-4fcb-815e-d85b900184a6/image.png 'image.png')编译按钮，等待代码编译无报错后，单击![image.png](https://raw.gitcode.com/user-images/assets/8737315/f03e2e73-e38d-4215-b407-512d8731aed8/image.png 'image.png')烧录按钮即可将控制代码烧录到STM32的主控中。

![image.png](https://raw.gitcode.com/user-images/assets/8737315/c06859bd-9720-48c0-8612-fc8e586ea1a7/image.png 'image.png')

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