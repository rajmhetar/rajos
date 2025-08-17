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
 * Enhanced demo task functions
 */
static void demo_task_1(void)
{
    uint32_t counter = 0;
    uint32_t last_report = 0;
    
    uart_puts("Demo Task 1: Starting interactive counter...\n");
    
    while (1) {
        counter++;
        
        /* Report every 5 seconds with different messages */
        if ((counter & 0x1387) == 0) {  /* Every 5000 ticks */
            uint32_t seconds = counter >> 10;  /* Divide by 1024 (close to 1000) */
            uart_printf("Task 1: Running for %d seconds (Counter: %d)\n", seconds, counter);
            
            /* Show different behaviors based on time */
            if ((seconds & 0xF) == 0) {  /* Every 16 seconds (close to 10) */
                uart_puts("   Task 1: Milestone reached!\n");
            } else if ((seconds & 0x7) == 0) {  /* Every 8 seconds (close to 5) */
                uart_puts("   Task 1: Status check - all systems nominal\n");
            }
        }
        
        task_sleep(1000);  /* Sleep for 1 second */
    }
}

static void demo_task_2(void)
{
    uint32_t counter = 0;
    uint32_t pattern = 0;
    
    uart_puts("🎲 Demo Task 2: Starting pattern generator...\n");
    
    while (1) {
        counter++;
        pattern = (pattern + 1) & 0xF;  /* Keep in range 0-15 */
        
        /* Report every 2 seconds with visual patterns */
        if ((counter & 0x7FF) == 0) {  /* Every 2048 ticks */
            uint32_t seconds = counter >> 10;  /* Divide by 1024 */
            uart_printf("Task 2: Pattern %d at %d seconds\n", pattern, seconds);
            
            /* Create a visual pattern */
            uart_puts("   Pattern: ");
            for (int i = 0; i < 16; i++) {
                if (i == pattern) {
                    uart_puts("*");
                } else {
                    uart_puts("-");
                }
            }
            uart_puts("\n");
        }
        
        task_sleep(2000);  /* Sleep for 2 seconds */
    }
}

static void demo_task_3(void)
{
    uint32_t counter = 0;
    const char* messages[] = {
        "Hello from Task 3!",
        "RajOS is awesome!",
        "Real-time systems rule!",
        "ARM assembly is fun!",
        "Embedded programming rocks!"
    };
    uint32_t msg_index = 0;
    
    uart_puts("Demo Task 3: Starting message broadcaster...\n");
    
    while (1) {
        counter++;
        
        /* Broadcast a message every 3 seconds */
        if ((counter & 0xBFF) == 0) {  /* Every 3072 ticks */
            uint32_t seconds = counter >> 10;  /* Divide by 1024 */
            uart_printf("Task 3: %s (at %d seconds)\n", 
                       messages[msg_index], seconds);
            
            msg_index = (msg_index + 1) & 0x3;  /* Keep in range 0-4 */
        }
        
        task_sleep(3000);  /* Sleep for 3 seconds */
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
    uart_puts("SUCCESS: UART driver initialized\n");
    
    /* Initialize system timer */
    timer_init(TIMER_DEFAULT_FREQUENCY_HZ);
    timer_start();
    uart_puts("SUCCESS: System timer initialized\n");
    
    /* Create enhanced demo tasks */
    task_tcb_t *task1 = task_create("DemoTask1", demo_task_1, TASK_PRIORITY_NORMAL, TASK_DEFAULT_STACK_SIZE);
    task_tcb_t *task2 = task_create("DemoTask2", demo_task_2, TASK_PRIORITY_NORMAL, TASK_DEFAULT_STACK_SIZE);
    task_tcb_t *task3 = task_create("DemoTask3", demo_task_3, TASK_PRIORITY_NORMAL, TASK_DEFAULT_STACK_SIZE);
    
    if (task1 && task2 && task3) {
        uart_puts("SUCCESS: All demo tasks created successfully\n");
        uart_printf("   Created %d tasks with different behaviors\n", 3);
    } else {
        uart_puts("ERROR: Failed to create some demo tasks\n");
    }
    
    uart_puts("SUCCESS: Kernel initialization complete\n");
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
    uart_puts("System ready for multitasking...\n");
    uart_puts("Watch the demo tasks in action:\n");
    uart_puts("   • Task 1: Interactive counter (every 1s)\n");
    uart_puts("   • Task 2: Pattern generator (every 2s)\n");
    uart_puts("   • Task 3: Message broadcaster (every 3s)\n");
    uart_puts("   • Timer: System heartbeat (every 1s)\n");
    uart_puts("   • Kernel: Main loop status (every 5s)\n\n");
    
    /* Main kernel loop */
    uint32_t counter = 0;
    while (1) {
        /* Simple heartbeat to show the system is alive */
        if ((counter & 0xF423F) == 0) {  /* Every 1,000,000 ticks */
            uint32_t heartbeat = counter >> 20;  /* Divide by 1,048,576 */
            uart_printf("Kernel heartbeat: %d\n", heartbeat);
        }
        counter++;
        
        /* TODO: Implement proper task scheduling here */
        /* For now, just loop to demonstrate the kernel is running */
        
        /* Simple delay to prevent overwhelming the output */
        if ((counter & 0x4C4B3F) == 0) {  /* Every 5,000,000 ticks */
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
    uart_puts("FATAL ERROR: ");
    uart_puts(message);
    uart_puts("\nSystem halted.\n");
    
    /* Disable interrupts and halt */
    __asm volatile (
        "mrs r0, cpsr\n"
        "orr r0, r0, #0xC0\n"
        "msr cpsr, r0"
    );
    while (1) {
        /* Infinite loop */
    }
}