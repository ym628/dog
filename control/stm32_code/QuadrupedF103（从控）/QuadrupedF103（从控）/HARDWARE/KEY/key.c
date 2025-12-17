#include "key.h"

/**************************************************************************
函数功能：按键初始化
入口参数：无
返回  值：无 
**************************************************************************/
void KEY_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStructure;
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE); //使能端口时钟
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_14;	            //端口配置
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;         //上拉输入
  GPIO_Init(GPIOB, &GPIO_InitStructure);					      //根据设定参数初始化GPIO
} 

/**************************************************************************
函数功能：按键扫描
入口参数：无
返回  值：按键状态 0：无动作 1：单击 
**************************************************************************/
u8 click(void)
{
			static u8 flag_key=1;//按键按松开标志
			if(flag_key&&KEY==0)
			{
			flag_key=0;
			return 1;	// 按键按下
			}
			else if(1==KEY)			flag_key=1;
			return 0;//无按键按下
}
/**************************************************************************
函数功能：长按检测
入口参数：无
返 回 值：按键状态 0：无动作  1：长按
**************************************************************************/
u8 Long_Press(void)
{
	static int PressCount;
	int Pressed,PressTimeCount=10;
	if(KEY==0&&PressCount<(PressTimeCount+1)) PressCount++;
	if(KEY==1)
	{
		Delay_ms();
		if(KEY==1)PressCount=0,Pressed=0;
	}
	if((PressTimeCount)==PressCount) Pressed=1;
	
	if(Pressed==1) 
	{
		Pressed=0;
		return 1;
	}
	else return 0;
}
/**************************************************************************
函数功能：延迟函数
入口参数：无
返 回 值：无
**************************************************************************/
void Delay_ms(void)
{
   int ii,i;    
   for(ii=0;ii<50;ii++)
   {
	   for(i=0;i<500;i++);
	 }	
}
