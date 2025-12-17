#ifndef _ENCODER_H
#define _ENCODER_H
#include "sys.h"
#include "system.h"

#define ENCODER_TIM_PERIOD (u16)(65535)   //不可大于65535 因为定时器是16位的。
 
typedef struct
{
int M1;
int M2;
int M3;
int M4;
} EncoderState_t;
extern EncoderState_t EncoderState;

void Encoder_Init_TIM2(void);
void Encoder_Init_TIM3(void);
void Encoder_Init_TIM4(void);
void Encoder_Init_TIM5(void);
int Read_Encoder(u8 TIMX);
void UpdataEncoder(void);
void TIM2_IRQHandler(void);
void TIM3_IRQHandler(void);
void TIM4_IRQHandler(void);
void TIM5_IRQHandler(void);
#endif
