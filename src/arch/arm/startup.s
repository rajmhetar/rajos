/*
 * RajOS Startup Code
 * ARM Cortex-M Assembly
 * 
 * This file contains:
 * - Vector table with exception handlers
 * - Reset handler that initializes the system
 * - Default exception handlers
 */

.syntax unified
.cpu cortex-m3
.thumb

/* Linker symbols defined in linker.ld */
.extern _stack_top
.extern _data_start
.extern _data_end  
.extern _data_load_start
.extern _bss_start
.extern _bss_end

/* C functions from kernel and drivers */
.extern kernel_main
.extern timer_tick_callback

.section .vectors, "a"
.align 2

/*
 * Vector Table
 * ARM Cortex-M requires this at address 0x00000000
 * First entry: initial stack pointer
 * Second entry: reset handler address  
 * Remaining entries: exception/interrupt handlers
 */
.global vector_table
vector_table:
    .word _stack_top              /* 0x00: Initial stack pointer */
    .word Reset_Handler + 1       /* 0x04: Reset handler (+1 for Thumb mode) */
    .word NMI_Handler + 1         /* 0x08: Non-maskable interrupt */
    .word HardFault_Handler + 1   /* 0x0C: Hard fault */
    .word MemManage_Handler + 1   /* 0x10: Memory management fault */
    .word BusFault_Handler + 1    /* 0x14: Bus fault */
    .word UsageFault_Handler + 1  /* 0x18: Usage fault */
    .word 0                       /* 0x1C: Reserved */
    .word 0                       /* 0x20: Reserved */
    .word 0                       /* 0x24: Reserved */
    .word 0                       /* 0x28: Reserved */
    .word SVC_Handler + 1         /* 0x2C: Supervisor call */
    .word DebugMon_Handler + 1    /* 0x30: Debug monitor */
    .word 0                       /* 0x34: Reserved */
    .word PendSV_Handler + 1      /* 0x38: PendSV (context switching) */
    .word SysTick_Handler + 1     /* 0x3C: System tick timer */
    
    /* External interrupts (first 16) */
    .word IRQ_Handler + 1         /* IRQ 0 */
    .word IRQ_Handler + 1         /* IRQ 1 */
    .word IRQ_Handler + 1         /* IRQ 2 */
    .word IRQ_Handler + 1         /* IRQ 3 */
    .word IRQ_Handler + 1         /* IRQ 4 */
    .word IRQ_Handler + 1         /* IRQ 5 */
    .word IRQ_Handler + 1         /* IRQ 6 */
    .word IRQ_Handler + 1         /* IRQ 7 */
    .word IRQ_Handler + 1         /* IRQ 8 */
    .word IRQ_Handler + 1         /* IRQ 9 */
    .word IRQ_Handler + 1         /* IRQ 10 */
    .word IRQ_Handler + 1         /* IRQ 11 */
    .word IRQ_Handler + 1         /* IRQ 12 */
    .word IRQ_Handler + 1         /* IRQ 13 */
    .word IRQ_Handler + 1         /* IRQ 14 */
    .word IRQ_Handler + 1         /* IRQ 15 */

.section .text

/*
 * Reset Handler
 * Called when the processor starts up
 * Responsible for system initialization before jumping to C code
 */
.global Reset_Handler
.type Reset_Handler, %function
Reset_Handler:
    /* Disable interrupts during startup */
    cpsid i
    
    /* Copy initialized data from flash to RAM */
    ldr r0, =_data_start          /* Destination (RAM) */
    ldr r1, =_data_load_start     /* Source (Flash) */
    ldr r2, =_data_end            /* End of data in RAM */
    
data_copy_loop:
    cmp r0, r2                    /* Check if we're done */
    bge data_copy_done
    ldr r3, [r1], #4              /* Load from flash, increment source */
    str r3, [r0], #4              /* Store to RAM, increment destination */
    b data_copy_loop
data_copy_done:

    /* Zero out BSS section (uninitialized variables) */
    ldr r0, =_bss_start           /* Start of BSS */
    ldr r1, =_bss_end             /* End of BSS */
    mov r2, #0                    /* Zero value */
    
bss_zero_loop:
    cmp r0, r1                    /* Check if we're done */
    bge bss_zero_done
    str r2, [r0], #4              /* Store zero, increment address */
    b bss_zero_loop
bss_zero_done:

    /* Set up main stack pointer (already set by hardware, but good practice) */
    ldr r0, =_stack_top
    msr msp, r0
    
    /* Enable interrupts */
    cpsie i
    
    /* Jump to C kernel main function */
    bl kernel_main
    
    /* If kernel_main returns, loop forever */
infinite_loop:
    b infinite_loop

/*
 * Default Exception Handlers
 * These are called when exceptions occur
 * For now, they just loop forever (can be improved later)
 */

.global NMI_Handler
.type NMI_Handler, %function
NMI_Handler:
    b NMI_Handler

.global HardFault_Handler  
.type HardFault_Handler, %function
HardFault_Handler:
    b HardFault_Handler

.global MemManage_Handler
.type MemManage_Handler, %function  
MemManage_Handler:
    b MemManage_Handler

.global BusFault_Handler
.type BusFault_Handler, %function
BusFault_Handler:
    b BusFault_Handler

.global UsageFault_Handler
.type UsageFault_Handler, %function
UsageFault_Handler:
    b UsageFault_Handler

.global SVC_Handler
.type SVC_Handler, %function
SVC_Handler:
    b SVC_Handler

.global DebugMon_Handler
.type DebugMon_Handler, %function
DebugMon_Handler:
    b DebugMon_Handler

.global PendSV_Handler
.type PendSV_Handler, %function
PendSV_Handler:
    b PendSV_Handler

.global SysTick_Handler
.type SysTick_Handler, %function
SysTick_Handler:
    /* Save registers */
    push {r0, r1, r2, r3, r12, lr}
    
    /* Call timer callback function */
    bl timer_tick_callback
    
    /* Restore registers */
    pop {r0, r1, r2, r3, r12, lr}
    
    /* Return from interrupt */
    bx lr

.global IRQ_Handler
.type IRQ_Handler, %function
IRQ_Handler:
    b IRQ_Handler

.end