#include "system.h"

//任务优先级
#define START_TASK_PRIO			1
//任务堆栈大小	
#define START_STK_SIZE 			256  
//任务句柄
TaskHandle_t StartTask_Handler; 
//任务函数
void start_task(void *pvParameters);

int main(void)
{ 
	systemInit();
	
	//创建开始任务
    xTaskCreate((TaskFunction_t )start_task,            //任务函数
                (const char*    )"start_task",          //任务名称
                (uint16_t       )START_STK_SIZE,        //任务堆栈大小
                (void*          )NULL,                  //传递给任务函数的参数
                (UBaseType_t    )START_TASK_PRIO,       //任务优先级
                (TaskHandle_t*  )&StartTask_Handler);   //任务句柄              
    vTaskStartScheduler();          //开启任务调度
}

//开始任务任务函数
void start_task(void *pvParameters)
{
  taskENTER_CRITICAL();           //进入临界区
  //创建任务
	xTaskCreate(Quadruped_task, "quadruped_task", QUADRUPED_STK_SIZE, NULL, QUADRUPED_TASK_PRIO, NULL);	//四足控制
	
	xTaskCreate(MPU6050_task, "MPU6050_task", MPU6050_STK_SIZE, NULL, MPU6050_TASK_PRIO, NULL);	//陀螺仪
	
  xTaskCreate(show_task, "show_task", SHOW_STK_SIZE, NULL,SHOW_TASK_PRIO, NULL); //显示屏显示
	
  xTaskCreate(led_task, "led_task", LED_STK_SIZE, NULL, LED_TASK_PRIO, NULL);	//led灯
	
	xTaskCreate(bee_task, "bee_task", BEE_STK_SIZE, NULL, BEE_TASK_PRIO, NULL);	//蜂鸣器
	
	xTaskCreate(key_task, "key_task", KEY_STK_SIZE, NULL, KEY_TASK_PRIO, NULL);		//用户按键	

	xTaskCreate(sent_task, "sent_task", SENT_STK_SIZE, NULL, SENT_TASK_PRIO, NULL);		//串口发送数据	
	
	xTaskCreate(getcontrol_task, "getcontrol_task", GETCONTROL_STK_SIZE, NULL, GETCONTROL_TASK_PRIO, NULL);	//获取控制信息	
	
  //xTaskCreate(pstwo_task, "PSTWO_task",PSTTWO_STK_SIZE , NULL, PSTWO_TASK_PRIO, NULL);	 //手柄控制 
	
	xTaskCreate(Remote_Check_task, "REMOTE_Check_task",REMOTE_CHECK_STK_SIZE , NULL, REMOTE_CHECK_TASK_PRIO, NULL);	 //进入航模遥控模式检测
	
  vTaskDelete(StartTask_Handler); //删除开始任务
	
  taskEXIT_CRITICAL();            //退出临界区
}

void SoftReset(void)
{
	  __set_FAULTMASK(1); // 关闭所有中断
    NVIC_SystemReset(); // 软件复位
}
 


