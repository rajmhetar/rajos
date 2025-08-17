/*
 * RajOS System Timer Driver
 * SysTick timer implementation for ARM
 * 
 * Author: Raj Mhetar
 */

#include "drivers/timer.h"
#include "drivers/uart.h"

/* Timer registers for QEMU versatileab (ARM926EJ-S) */
/* Using the system timer at 0x10011000 */
#define TIMER_BASE        0x10011000
#define TIMER_LOAD        (*(volatile uint32_t*)(TIMER_BASE + 0x00))
#define TIMER_VALUE       (*(volatile uint32_t*)(TIMER_BASE + 0x04))
#define TIMER_CTRL        (*(volatile uint32_t*)(TIMER_BASE + 0x08))
#define TIMER_CLEAR       (*(volatile uint32_t*)(TIMER_BASE + 0x0C))

/* Control register bits */
#define TIMER_CTRL_ENABLE     (1 << 7)
#define TIMER_CTRL_PERIODIC   (1 << 6)
#define TIMER_CTRL_INTEN      (1 << 5)

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
    /* Assuming 24MHz system clock - use fixed values to avoid division */
    uint32_t reload_value;
    if (frequency_hz == 1000) {
        reload_value = 23999;  /* 24MHz / 1000Hz - 1 */
    } else if (frequency_hz == 100) {
        reload_value = 239999;  /* 24MHz / 100Hz - 1 */
    } else {
        reload_value = 23999999;  /* Default: 1Hz */
    }
    
    /* Configure timer */
    TIMER_LOAD = reload_value;
    TIMER_VALUE = 0;  /* Clear current value */
    
    /* Enable timer with interrupts, periodic mode */
    TIMER_CTRL = TIMER_CTRL_ENABLE | TIMER_CTRL_PERIODIC | TIMER_CTRL_INTEN;
    
    uart_printf("Timer initialized at %d Hz\n", frequency_hz);
}

/*
 * Start the timer
 */
void timer_start(void)
{
    TIMER_CTRL |= TIMER_CTRL_ENABLE;
    uart_puts("Timer started\n");
}

/*
 * Stop the timer
 */
void timer_stop(void)
{
    TIMER_CTRL &= ~TIMER_CTRL_ENABLE;
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
        /* Simple busy wait for ARM926EJ-S compatibility */
        /* In a real system, this would use proper task scheduling */
        volatile uint32_t i;
        for (i = 0; i < 1000; i++) { }
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
    if ((timer_ticks & 0x3FF) == 0) {  /* Every 1024 ticks */
        uart_printf("Timer tick: %d\n", timer_ticks);
    }
}
