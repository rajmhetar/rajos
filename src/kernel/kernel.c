/*
 * RajOS Kernel Main
 * Entry point for the RajOS kernel
 */

#include "kernel/types.h"
#include "drivers/uart.h"
#include "drivers/timer.h"
#include "kernel/task.h"

/* Kernel version information */
#define RAJOS_VERSION_MAJOR  0
#define RAJOS_VERSION_MINOR  1
#define RAJOS_VERSION_PATCH  0

/*
 * Display kernel banner
 */
static void print_banner(void)
{
    uart_puts("\n");
    uart_puts("========================================\n");
    uart_puts("         RajOS v");
    uart_printf("%d.%d.%d", RAJOS_VERSION_MAJOR, RAJOS_VERSION_MINOR, RAJOS_VERSION_PATCH);
    uart_puts("\n");
    uart_puts("  Custom Real-Time Operating System\n");
    uart_puts("     Built from scratch in C/ARM\n");
    uart_puts("========================================\n");
    uart_puts("\n");
}

/*
 * Demo task functions
 */
static void demo_task_1(void)
{
    uint32_t counter = 0;
    while (1) {
        uart_printf("Demo Task 1: Counter = %d\n", counter++);
        task_sleep(1000);  /* Sleep for 1 second */
    }
}

static void demo_task_2(void)
{
    uint32_t counter = 0;
    while (1) {
        uart_printf("Demo Task 2: Counter = %d\n", counter++);
        task_sleep(2000);  /* Sleep for 2 seconds */
    }
}

/*
 * Initialize kernel subsystems
 */
static void kernel_init(void)
{
    uart_puts("Initializing RajOS kernel...\n");
    
    /* Initialize UART first for console output */
    uart_init();
    uart_puts("UART driver initialized\n");
    
    /* Initialize system timer */
    timer_init(TIMER_DEFAULT_FREQUENCY_HZ);
    timer_start();
    uart_puts("System timer initialized\n");
    
    /* Create demo tasks */
    task_tcb_t *task1 = task_create("DemoTask1", demo_task_1, TASK_PRIORITY_NORMAL, TASK_DEFAULT_STACK_SIZE);
    task_tcb_t *task2 = task_create("DemoTask2", demo_task_2, TASK_PRIORITY_NORMAL, TASK_DEFAULT_STACK_SIZE);
    
    if (task1 && task2) {
        uart_puts("Demo tasks created successfully\n");
    } else {
        uart_puts("Failed to create demo tasks\n");
    }
    
    uart_puts("Kernel initialization complete\n");
}

/*
 * Main kernel entry point
 * Called from startup.s after system initialization
 */
void kernel_main(void)
{
    /* Initialize all kernel subsystems */
    kernel_init();
    
    /* Display startup banner */
    print_banner();
    
    uart_puts("RajOS is now running!\n");
    uart_puts("System ready for multitasking...\n\n");
    
    /* Main kernel loop */
    uint32_t counter = 0;
    while (1) {
        /* Simple heartbeat to show the system is alive */
        if (counter % 1000000 == 0) {
            uart_printf("Kernel heartbeat: %d\n", counter / 1000000);
        }
        counter++;
        
        /* TODO: Implement proper task scheduling here */
        /* For now, just loop to demonstrate the kernel is running */
        
        /* Simple delay to prevent overwhelming the output */
        if (counter % 5000000 == 0) {
            uart_puts("Main kernel loop running...\n");
        }
    }
}

/*
 * Kernel panic function
 * Called when an unrecoverable error occurs
 */
void kernel_panic(const char *message)
{
    uart_puts("\n*** KERNEL PANIC ***\n");
    uart_puts("Fatal error: ");
    uart_puts(message);
    uart_puts("\nSystem halted.\n");
    
    /* Disable interrupts and halt */
    __asm volatile ("cpsid i");
    while (1) {
        /* Infinite loop */
    }
}