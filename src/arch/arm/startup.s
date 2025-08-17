/*
 * RajOS Startup Code
 * ARM926EJ-S Assembly
 * 
 * This file contains:
 * - Vector table with exception handlers
 * - Reset handler that initializes the system
 * - Default exception handlers
 */

.syntax unified
.cpu arm926ej-s
.arm

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
.align 4

/*
 * Vector Table for ARM926EJ-S
 * ARM926 requires this at address 0x00000000
 * Different format from Cortex-M
 */
.global vector_table
vector_table:
    ldr pc, =Reset_Handler        /* 0x00: Reset */
    ldr pc, =Undefined_Handler    /* 0x04: Undefined instruction */
    ldr pc, =SVC_Handler          /* 0x08: Software interrupt */
    ldr pc, =Prefetch_Handler     /* 0x0C: Prefetch abort */
    ldr pc, =Data_Handler         /* 0x10: Data abort */
    ldr pc, =IRQ_Handler          /* 0x14: IRQ */
    ldr pc, =FIQ_Handler          /* 0x18: FIQ */

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
    mrs r3, cpsr
    orr r3, r3, #0xC0    /* Set IRQ and FIQ disable bits */
    msr cpsr, r3
    
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

    /* Set up main stack pointer for ARM926 */
    ldr sp, =_stack_top
    
    /* Enable interrupts */
    mrs r3, cpsr
    bic r3, r3, #0xC0    /* Clear IRQ and FIQ disable bits */
    msr cpsr, r3
    
    /* Jump to C kernel main function */
    bl kernel_main
    
    /* If kernel_main returns, loop forever */
infinite_loop:
    b infinite_loop

/*
 * Default Exception Handlers for ARM926
 * These are called when exceptions occur
 * For now, they just loop forever (can be improved later)
 */

.global Undefined_Handler
.type Undefined_Handler, %function
Undefined_Handler:
    b Undefined_Handler

.global SVC_Handler
.type SVC_Handler, %function
SVC_Handler:
    b SVC_Handler

.global Prefetch_Handler
.type Prefetch_Handler, %function
Prefetch_Handler:
    b Prefetch_Handler

.global Data_Handler
.type Data_Handler, %function
Data_Handler:
    b Data_Handler

.global IRQ_Handler
.type IRQ_Handler, %function
IRQ_Handler:
    b IRQ_Handler

.global FIQ_Handler
.type FIQ_Handler, %function
FIQ_Handler:
    b FIQ_Handler