/*
 * RajOS Task Management Implementation
 * Task creation, deletion, and state management
 * 
 * Author: Raj Mhetar
 */

#include "kernel/task.h"
#include "drivers/uart.h"

/* Simple string functions since we don't have standard library */
static void strncpy_safe(char *dest, const char *src, size_t n)
{
    size_t i;
    for (i = 0; i < n && src[i] != '\0'; i++) {
        dest[i] = src[i];
    }
    /* Ensure null termination */
    if (i < n) {
        dest[i] = '\0';
    }
}

/* Global variables */
static uint32_t next_task_id = 1;
static task_tcb_t *task_list = NULL;
static task_tcb_t *current_task = NULL;

/* Memory allocation (simple implementation for now) */
static uint8_t task_heap[32768];  /* 32KB for task stacks */
static uint32_t heap_ptr = 0;

/*
 * Simple memory allocation for task stacks
 */
static void* task_malloc(uint32_t size)
{
    if (heap_ptr + size > sizeof(task_heap)) {
        return NULL;  /* Out of memory */
    }
    
    void *ptr = &task_heap[heap_ptr];
    heap_ptr += size;
    return ptr;
}

/*
 * Create a new task
 */
task_tcb_t* task_create(const char *name, void (*entry_point)(void), 
                        task_priority_t priority, uint32_t stack_size)
{
    /* Validate parameters */
    if (!entry_point || !name || stack_size < TASK_MIN_STACK_SIZE) {
        uart_puts("Invalid task parameters\n");
        return NULL;
    }
    
    /* Allocate TCB */
    task_tcb_t *tcb = (task_tcb_t*)task_malloc(sizeof(task_tcb_t));
    if (!tcb) {
        uart_puts("Failed to allocate TCB\n");
        return NULL;
    }
    
    /* Allocate stack */
    uint32_t *stack = (uint32_t*)task_malloc(stack_size);
    if (!stack) {
        uart_puts("Failed to allocate stack\n");
        return NULL;
    }
    
    /* Initialize TCB */
    tcb->task_id = next_task_id++;
    strncpy_safe(tcb->name, name, TASK_MAX_NAME_LENGTH);
    
    tcb->state = TASK_STATE_READY;
    tcb->priority = priority;
    tcb->entry_point = entry_point;
    
    tcb->stack_start = stack;
    tcb->stack_size = stack_size;
    tcb->stack_ptr = stack + (stack_size / 4) - 1;  /* Stack grows downward */
    
    tcb->wake_time = 0;
    tcb->time_slice = 10;  /* 10ms default time slice */
    tcb->time_used = 0;
    tcb->context_switches = 0;
    tcb->total_runtime = 0;
    
    /* Initialize stack with initial context (simplified) */
    /* For now, we'll just set up a basic stack frame */
    tcb->stack_ptr[0] = 0x01000000;  /* xPSR (Thumb mode) */
    tcb->stack_ptr[-1] = (uint32_t)entry_point;  /* PC */
    tcb->stack_ptr[-2] = 0xFFFFFFFD;  /* LR (return to thread mode) */
    tcb->stack_ptr[-3] = 0;  /* R12 */
    tcb->stack_ptr[-4] = 0;  /* R3 */
    tcb->stack_ptr[-5] = 0;  /* R2 */
    tcb->stack_ptr[-6] = 0;  /* R1 */
    tcb->stack_ptr[-7] = 0;  /* R0 */
    
    /* Adjust stack pointer to point to R0 */
    tcb->stack_ptr -= 7;
    
    /* Add to task list */
    tcb->next = task_list;
    task_list = tcb;
    
    uart_printf("Task '%s' created (ID: %d, Priority: %d)\n", 
                name, tcb->task_id, priority);
    
    return tcb;
}

/*
 * Delete a task
 */
void task_delete(task_tcb_t *task)
{
    if (!task) return;
    
    /* Remove from task list */
    if (task_list == task) {
        task_list = task->next;
    } else {
        task_tcb_t *prev = task_list;
        while (prev && prev->next != task) {
            prev = prev->next;
        }
        if (prev) {
            prev->next = task->next;
        }
    }
    
    uart_printf("Task '%s' deleted\n", task->name);
    
    /* Note: In a real system, we'd free the memory here */
    /* For now, we'll just mark it as invalid */
    task->state = TASK_STATE_INVALID;
}

/*
 * Suspend a task
 */
void task_suspend(task_tcb_t *task)
{
    if (!task || task->state == TASK_STATE_INVALID) return;
    
    if (task->state == TASK_STATE_RUNNING) {
        task->state = TASK_STATE_SUSPENDED;
        uart_printf("Task '%s' suspended\n", task->name);
    }
}

/*
 * Resume a suspended task
 */
void task_resume(task_tcb_t *task)
{
    if (!task || task->state != TASK_STATE_SUSPENDED) return;
    
    task->state = TASK_STATE_READY;
    uart_printf("Task '%s' resumed\n", task->name);
}

/*
 * Put current task to sleep
 */
void task_sleep(uint32_t milliseconds)
{
    if (!current_task) return;
    
    current_task->state = TASK_STATE_SLEEPING;
    current_task->wake_time = current_task->wake_time + milliseconds;
    
    uart_printf("Task '%s' sleeping for %d ms\n", 
                current_task->name, milliseconds);
    
    /* TODO: Implement proper sleep with timer */
}

/*
 * Yield CPU to another task
 */
void task_yield(void)
{
    if (!current_task) return;
    
    uart_printf("Task '%s' yielding\n", current_task->name);
    
    /* TODO: Implement context switching */
    /* For now, just mark as ready */
    current_task->state = TASK_STATE_READY;
}

/*
 * Get task state
 */
task_state_t task_get_state(task_tcb_t *task)
{
    return task ? task->state : TASK_STATE_INVALID;
}

/*
 * Get task priority
 */
task_priority_t task_get_priority(task_tcb_t *task)
{
    return task ? task->priority : TASK_PRIORITY_IDLE;
}

/*
 * Get task ID
 */
uint32_t task_get_id(task_tcb_t *task)
{
    return task ? task->task_id : 0;
}

/*
 * Get current task
 */
task_tcb_t* task_get_current(void)
{
    return current_task;
}

/*
 * Set current task
 */
void task_set_current(task_tcb_t *task)
{
    current_task = task;
}
