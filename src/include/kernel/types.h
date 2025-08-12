/*
 * RajOS Basic Types
 * Standard type definitions for the kernel
 */

#ifndef TYPES_H
#define TYPES_H

/* Standard integer types */
typedef unsigned char      uint8_t;
typedef unsigned short     uint16_t;
typedef unsigned int       uint32_t;
typedef unsigned long long uint64_t;

typedef signed char        int8_t;
typedef signed short       int16_t;
typedef signed int         int32_t;
typedef signed long long   int64_t;

/* Pointer and size types */
typedef uint32_t           uintptr_t;
typedef int32_t            intptr_t;
typedef uint32_t           size_t;

/* Boolean type */
typedef enum {
    false = 0,
    true = 1
} bool;

/* NULL pointer */
#ifndef NULL
#define NULL ((void*)0)
#endif

/* Common constants */
#define KERNEL_SUCCESS  0
#define KERNEL_ERROR   -1

#endif /* TYPES_H */