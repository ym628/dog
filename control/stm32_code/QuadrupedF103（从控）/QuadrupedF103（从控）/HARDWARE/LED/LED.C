#include "led.h"

int Led_Count;//LED闪烁控制
/**************************************************************************
函数功能：LED接口初始化
入口参数：无 
返回  值：无
**************************************************************************/
void LED_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStructure;
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE); //使能端口时钟
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13;	            //端口配置
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;      //推挽输出
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;     //50M
  GPIO_Init(GPIOB, &GPIO_InitStructure);					      //根据设定参数初始化GPIO
	GPIO_SetBits(GPIOB,GPIO_Pin_13);
}
/**************************************************************************
函数功能：LED灯闪烁任务
入口参数：无 
返回  值：无
**************************************************************************/
void led_task(void *pvParameters)
{
    while(1)
    {
      LED=~LED;        //LED状态取反，0是点亮，1是熄灭                                  
      vTaskDelay(Led_Count); //相对延时函数，500MS改变一次状态
    }
}  

