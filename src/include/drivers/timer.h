/*
 * RajOS System Timer Driver Header
 * SysTick timer for periodic interrupts
 * 
 * Author: Raj Mhetar
 */

#ifndef TIMER_H
#define TIMER_H

#include "kernel/types.h"

/* Timer functions */
void timer_init(uint32_t frequency_hz);
void timer_start(void);
void timer_stop(void);
uint32_t timer_get_ticks(void);
void timer_delay_ms(uint32_t milliseconds);
void timer_tick_callback(void);

/* Timer configuration */
#define TIMER_DEFAULT_FREQUENCY_HZ  1000  /* 1ms tick period */
#define TIMER_MAX_FREQUENCY_HZ      10000 /* 0.1ms tick period */

#endif /* TIMER_H */
