/*
 * RajOS System Timer Driver
 * SysTick timer implementation for ARM
 * 
 * Author: Raj Mhetar
 */

#include "drivers/timer.h"
#include "drivers/uart.h"

/* SysTick registers (ARM Cortex-M style) */
#define SYSTICK_BASE      0xE000E010
#define SYSTICK_CTRL      (*(volatile uint32_t*)(SYSTICK_BASE + 0x00))
#define SYSTICK_LOAD      (*(volatile uint32_t*)(SYSTICK_BASE + 0x04))
#define SYSTICK_VAL       (*(volatile uint32_t*)(SYSTICK_BASE + 0x08))
#define SYSTICK_CALIB     (*(volatile uint32_t*)(SYSTICK_BASE + 0x0C)

/* Control register bits */
#define SYSTICK_CTRL_ENABLE      (1 << 0)
#define SYSTICK_CTRL_TICKINT     (1 << 1)
#define SYSTICK_CTRL_CLKSOURCE   (1 << 2)
#define SYSTICK_CTRL_COUNTFLAG   (1 << 16)

/* Global variables */
static uint32_t timer_ticks = 0;
static uint32_t timer_frequency_hz = 0;

/*
 * Initialize the system timer
 * frequency_hz: desired timer frequency in Hz
 */
void timer_init(uint32_t frequency_hz)
{
    /* Validate frequency */
    if (frequency_hz > TIMER_MAX_FREQUENCY_HZ) {
        frequency_hz = TIMER_MAX_FREQUENCY_HZ;
    }
    
    timer_frequency_hz = frequency_hz;
    
    /* Calculate reload value for desired frequency */
    /* Assuming 24MHz system clock */
    uint32_t reload_value = (24000000 / frequency_hz) - 1;
    
    /* Configure SysTick */
    SYSTICK_LOAD = reload_value;
    SYSTICK_VAL = 0;  /* Clear current value */
    
    /* Enable SysTick with interrupts, use processor clock */
    SYSTICK_CTRL = SYSTICK_CTRL_ENABLE | SYSTICK_CTRL_TICKINT | SYSTICK_CTRL_CLKSOURCE;
    
    uart_printf("Timer initialized at %d Hz\n", frequency_hz);
}

/*
 * Start the timer
 */
void timer_start(void)
{
    SYSTICK_CTRL |= SYSTICK_CTRL_ENABLE;
    uart_puts("Timer started\n");
}

/*
 * Stop the timer
 */
void timer_stop(void)
{
    SYSTICK_CTRL &= ~SYSTICK_CTRL_ENABLE;
    uart_puts("Timer stopped\n");
}

/*
 * Get current timer tick count
 */
uint32_t timer_get_ticks(void)
{
    return timer_ticks;
}

/*
 * Delay for specified milliseconds
 */
void timer_delay_ms(uint32_t milliseconds)
{
    uint32_t start_ticks = timer_ticks;
    uint32_t target_ticks = start_ticks + (milliseconds * timer_frequency_hz / 1000);
    
    while (timer_ticks < target_ticks) {
        /* Wait for timer interrupt */
        __asm volatile ("wfi");  /* Wait for interrupt */
    }
}

/*
 * Timer tick callback function
 * Called from SysTick_Handler in startup.s
 */
void timer_tick_callback(void)
{
    timer_ticks++;
    
    /* Simple heartbeat every 1000 ticks (1 second at 1kHz) */
    if (timer_ticks % 1000 == 0) {
        uart_printf("Timer tick: %d\n", timer_ticks);
    }
}
