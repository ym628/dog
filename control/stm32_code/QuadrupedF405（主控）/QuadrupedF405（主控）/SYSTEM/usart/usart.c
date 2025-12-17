#include "sys.h"
#include "usart.h"	
#include "system.h"
////////////////////////////////////////////////////////////////////////////////// 	 
 

//加入以下代码,支持printf函数,而不需要选择use MicroLIB	  
#if 1
#pragma import(__use_no_semihosting)             
//标准库需要的支持函数                 
struct __FILE 
{ 
	int handle; 
}; 

FILE __stdout;       
//定义_sys_exit()以避免使用半主机模式    
void _sys_exit(int x) 
{ 
	x = x; 
} 
//重定义fputc函数 
int fputc(int ch, FILE *f)
{      
	while((USART2->SR&0X40)==0);// 
	USART2->DR = (u8) ch;      
	return ch;
}
#endif
 
#if EN_USART1_RX   //如果使能了接收
//串口1中断服务程序
//注意,读取USARTx->SR能避免莫名其妙的错误   	
u8 USART_RX_BUF[USART_REC_LEN];     //接收缓冲,最大USART_REC_LEN个字节.
//接收状态
//bit15，	接收完成标志
//bit14，	接收到0x0d
//bit13~0，	接收到的有效字节数目
u16 USART_RX_STA=0;       //接收状态标记	
 

//////////////////////////////////////////////////////////////////
/**************************实现函数**********************************************
*功    能:		usart发送一个字节
********************************************************************************/
void usart1_send(u8 data)
{
	USART1->DR = data;
	while((USART1->SR&0x40)==0);	
}


/**************************************************************************
函数功能：串口1初始化
入口参数： bound:波特率
返回  值：无
**************************************************************************/
void uart1_init(u32 bound){
	
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA,ENABLE); //使能GPIOA时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);//使能USART1时钟

	GPIO_PinAFConfig(GPIOA,GPIO_PinSource9,GPIO_AF_USART1); //GPIOA9复用为USART1
	GPIO_PinAFConfig(GPIOA,GPIO_PinSource10,GPIO_AF_USART1); //GPIOA10复用为USART1

	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9 | GPIO_Pin_10; //GPIOA9与GPIOA10
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;//复用功能
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;	//速度50MHz
	GPIO_InitStructure.GPIO_OType = GPIO_OType_PP; //推挽复用输出
	GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP; //上拉
	GPIO_Init(GPIOA,&GPIO_InitStructure); //初始化PA9，PA10

	USART_InitStructure.USART_BaudRate = bound;//波特率设置
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
	USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
	USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//收发模式
	USART_Init(USART1, &USART_InitStructure); //初始化串口1
	USART_Cmd(USART1, ENABLE);  //使能串口1 
	
	USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);//开启串口接受中断
	
    NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;//串口中断通道
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=0;//抢占优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority =1;		//子优先级
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQ通道使能
	NVIC_Init(&NVIC_InitStructure);	//根据指定的参数初始化NVIC寄存器
	
}


/**************************************************************************
函数功能：串口2初始化
入口参数： bound:波特率
返回  值：无
**************************************************************************/
void usart2_init(u32 bound)
{
    GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);	//使能GPIO时钟
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);	//使能USART时钟
	
	GPIO_PinAFConfig(GPIOA,GPIO_PinSource2,GPIO_AF_USART2); //GPIO.A2.A3复用为USART2
	GPIO_PinAFConfig(GPIOA,GPIO_PinSource3,GPIO_AF_USART2); //GPIO.A2.A3复用为USART2
	
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2|GPIO_Pin_3; //C10
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;//复用功能
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;	//速度50MHz
	GPIO_InitStructure.GPIO_OType = GPIO_OType_PP; //推挽复用输出
	GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP; //上拉
    GPIO_Init(GPIOA, &GPIO_InitStructure);   

	USART_InitStructure.USART_BaudRate = bound;//串口波特率
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
	USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
	USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//收发模式
	USART_Init(USART2, &USART_InitStructure);     //初始化串口2
	
	USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);//开启串口接受中断
	USART_Cmd(USART2, ENABLE);                    //使能串口2
		
    NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=0 ;//抢占优先级
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;		//子优先级
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQ通道使能
	NVIC_Init(&NVIC_InitStructure);	//根据指定的参数初始化VIC寄存器
}

/**************************************************************************
函数功能：串口1中断服务函数
入口参数：无
返回  值：无
**************************************************************************/
void USART1_IRQHandler(void)                	//串口1中断服务程序
{
	u8 Res;
	
	if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)  //接收中断(接收到的数据必须是0x0d 0x0a结尾)
	{
		Res =USART_ReceiveData(USART1);//(USART1->DR);	//读取接收到的数据
		
		if((USART_RX_STA&0x8000)==0)//接收未完成
		{
			if(USART_RX_STA&0x4000)//接收到了0x0d
			{
				if(Res!=0x0a)USART_RX_STA=0;//接收错误,重新开始
				else USART_RX_STA|=0x8000;	//接收完成了 
			}
			else //还没收到0X0D
			{	
				if(Res==0x0d)USART_RX_STA|=0x4000;
				else
				{
					USART_RX_BUF[USART_RX_STA&0X3FFF]=Res ;
					USART_RX_STA++;
					if(USART_RX_STA>(USART_REC_LEN-1))USART_RX_STA=0;//接收数据错误,重新开始接收	  
				}		 
			}
		}   		 
  } 
	
}

/**************************************************************************
函数功能：串口2中断服务函数
入口参数：无
返回  值：无
**************************************************************************/
u8 Usart2_Receive=0X5A;
u8 Usart_Receive;
int USART2_IRQHandler(void)
{	
	static	int uart_receive=0;  
	static u8 Flag_PID,i,j,Receive[50];
  static float Data;	
	if(USART_GetITStatus(USART2, USART_IT_RXNE) != RESET) //接收到数据
	{	        
		uart_receive=USART2->DR; 
    Usart_Receive = uart_receive ; 
    Remote_count=0;		
		if(APP_ON_Flag==0&&start_up_15_second==1) APP_ON_Flag=1,PS2_ON_Flag=0,USART_ON_FLAG=0,Remote_ON_Flag=0;
		      if(Usart_Receive==0x4B)    Turn_Flag=2;  //进入转向控制界面
	  else	if(Usart_Receive==0x4A) 	 Turn_Flag=1;	//方向控制界面	
		else  if(Usart_Receive==0x49)    APP_KEY=15,Turn_Flag=0; //四足进入预备态
		
	  if(Usart_Receive==0x58)       
		{
		APP_START_STOP_FLAG=!APP_START_STOP_FLAG; //加速按键，控制四足站立和回收
		if(APP_START_STOP_FLAG==0) APP_KEY=4;
		else                       APP_KEY=16;
		}
		if(Usart_Receive==0x59)       APP_KEY=14; //减速按键，暂停运动
		
		if(Turn_Flag==1)//摇杆控制界面
		{
				if(Usart_Receive>=0x41&&Usart_Receive<=0x48)  
				{	
					Flag_Direction=Usart_Receive-0x40;
				}
				else	if(Usart_Receive<=8)   
				{			
					Flag_Direction=Usart_Receive;
				}	
				else  Flag_Direction=0;
		}
		else if(Turn_Flag==2)//按键控制界面
		{
			 if     (Usart_Receive==0x41) Flag_Pose=1; //前倾
			 else if(Usart_Receive==0x43) Flag_Pose=3; //右侧
			 else if(Usart_Receive==0x45) Flag_Pose=5; //后仰
			 else if(Usart_Receive==0x47) Flag_Pose=7; //左侧
			 else                         Flag_Pose=0; //无动作
		}
   }
	
	 	 //以下是与APP调试界面通讯
		 if(Usart_Receive==0x7B) Flag_PID=1;   //APP参数指令起始位
		 if(Usart_Receive==0x7D) Flag_PID=2;   //APP参数指令停止位

		 if(Flag_PID==1)  //采集数据
		 {
			Receive[i]=Usart_Receive;
			i++;
		 }
		 if(Flag_PID==2)  //分析数据
		 {
			     	if(Receive[3]==0x50) 	 PID_Send=1;
					 else  if(Receive[1]!=0x23) 
					 {								
						for(j=i;j>=4;j--)
						{
						  Data+=(Receive[j-1]-48)*pow(10,i-j);
						}
						switch(Receive[1])
						 {
							 case 0x30:  RC_Velocity=Data;break;
							 case 0x31:  break;
							 case 0x32:  break;
							 case 0x33:  break;
							 case 0x34:  break;
							 case 0x35:  break;
							 case 0x36:  break;
							 case 0x37:  break;
							 case 0x38:  break; 		//预留
						 }
					 }				 
					 Flag_PID=0;//相关标志位清零
					 i=0;
					 j=0;
					 Data=0;
					 memset(Receive, 0, sizeof(u8)*50);//数组清零
		 }
	
	 
return 0;	
}

/**************************************************************************
函数功能：串口扫描
**************************************************************************/
u8 click_RC (void)
{
			static u8 flag_key=1;//按键按松开标志
	    u8 temp;
			if(flag_key&&Usart2_Receive!=0x5A)
			{
			flag_key=0;
		  if(Usart2_Receive>=0x01&&Usart2_Receive<=0x08)temp=Usart2_Receive;
		  else	if(Usart2_Receive>=0x41&&Usart2_Receive<=0x48)temp=Usart2_Receive-0x40;	
		//	else 	temp=0;
			return temp;	// 按键按下
			}
			else if(Usart2_Receive==0x5A)			flag_key=1;
			return 0;//无按键按下
}

#endif	


 



