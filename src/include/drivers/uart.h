/*
 * RajOS UART Driver Header
 * Basic UART driver for console output
 */

#ifndef UART_H
#define UART_H

#include "kernel/types.h"

/* UART functions */
void uart_init(void);
void uart_putc(char c);
void uart_puts(const char *str);
void uart_printf(const char *format, ...);

#endif /* UART_H */