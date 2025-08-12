/*
 * RajOS Task Management Header
 * Task Control Block (TCB) and task management functions
 * 
 * Author: Raj Mhetar
 */

#ifndef TASK_H
#define TASK_H

#include "kernel/types.h"

/* Task states */
typedef enum {
    TASK_STATE_INVALID = 0,
    TASK_STATE_READY,
    TASK_STATE_RUNNING,
    TASK_STATE_BLOCKED,
    TASK_STATE_SLEEPING,
    TASK_STATE_SUSPENDED
} task_state_t;

/* Task priorities */
typedef enum {
    TASK_PRIORITY_IDLE = 0,
    TASK_PRIORITY_LOW = 1,
    TASK_PRIORITY_NORMAL = 2,
    TASK_PRIORITY_HIGH = 3,
    TASK_PRIORITY_CRITICAL = 4,
    TASK_PRIORITY_MAX = 5
} task_priority_t;

/* Task Control Block (TCB) */
typedef struct task_tcb {
    /* Task identification */
    uint32_t task_id;
    char name[16];
    
    /* Task state and priority */
    task_state_t state;
    task_priority_t priority;
    
    /* Stack management */
    uint32_t *stack_ptr;      /* Current stack pointer */
    uint32_t *stack_start;    /* Start of stack area */
    uint32_t stack_size;      /* Size of stack in bytes */
    
    /* Task function */
    void (*entry_point)(void);
    
    /* Timing and scheduling */
    uint32_t wake_time;       /* When to wake from sleep */
    uint32_t time_slice;      /* Time slice for round-robin */
    uint32_t time_used;       /* CPU time used */
    
    /* Next task in linked list */
    struct task_tcb *next;
    
    /* Task statistics */
    uint32_t context_switches;
    uint32_t total_runtime;
} task_tcb_t;

/* Task management functions */
task_tcb_t* task_create(const char *name, void (*entry_point)(void), 
                        task_priority_t priority, uint32_t stack_size);
void task_delete(task_tcb_t *task);
void task_suspend(task_tcb_t *task);
void task_resume(task_tcb_t *task);
void task_sleep(uint32_t milliseconds);
void task_yield(void);

/* Task state queries */
task_state_t task_get_state(task_tcb_t *task);
task_priority_t task_get_priority(task_tcb_t *task);
uint32_t task_get_id(task_tcb_t *task);

/* Additional task functions */
task_tcb_t* task_get_current(void);
void task_set_current(task_tcb_t *task);

/* Task configuration */
#define TASK_MIN_STACK_SIZE     512     /* 512 bytes minimum */
#define TASK_DEFAULT_STACK_SIZE 1024    /* 1KB default stack */
#define TASK_MAX_STACK_SIZE     8192    /* 8KB maximum stack */
#define TASK_MAX_NAME_LENGTH    15      /* Max name length */

#endif /* TASK_H */
