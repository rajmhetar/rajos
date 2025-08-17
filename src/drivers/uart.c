/*
 * RajOS UART Driver
 * Console output backend
 * - Default: PL011 UART on QEMU versatilepb (ARM9/ARM11 boards)
 * - Optional: Semihosting for Cortex-M (define RAJOS_SEMIHOSTING)
 */

#include "drivers/uart.h"

#ifndef RAJOS_SEMIHOSTING
/* PL011 UART0 registers for QEMU versatilepb */
#define UART0_BASE    0x101F1000
#define UART0_DR      (*(volatile uint32_t*)(UART0_BASE + 0x00))  /* Data register */
#define UART0_FR      (*(volatile uint32_t*)(UART0_BASE + 0x18))  /* Flag register */
#define UART0_IBRD    (*(volatile uint32_t*)(UART0_BASE + 0x24))  /* Integer baud rate */
#define UART0_FBRD    (*(volatile uint32_t*)(UART0_BASE + 0x28))  /* Fractional baud rate */
#define UART0_LCRH    (*(volatile uint32_t*)(UART0_BASE + 0x2C))  /* Line control */
#define UART0_CR      (*(volatile uint32_t*)(UART0_BASE + 0x30))  /* Control register */

/* Flag register bits */
#define UART_FR_TXFF  (1 << 5)  /* Transmit FIFO full */
#define UART_FR_RXFE  (1 << 4)  /* Receive FIFO empty */

/* Line control register bits */
#define UART_LCRH_WLEN_8BIT  (3 << 5)  /* 8-bit word length */
#define UART_LCRH_FEN        (1 << 4)  /* Enable FIFOs */

/* Control register bits */
#define UART_CR_UARTEN  (1 << 0)  /* UART enable */
#define UART_CR_TXE     (1 << 8)  /* Transmit enable */
#define UART_CR_RXE     (1 << 9)  /* Receive enable */
#endif /* !RAJOS_SEMIHOSTING */

/*
 * Initialize UART0 for basic console output
 */
void uart_init(void)
{
#ifdef RAJOS_SEMIHOSTING
    /* No hardware init needed for semihosting */
    (void)0;
#else
    /* Disable UART */
    UART0_CR = 0;
    /* Set baud rate to 115200 (assuming 24MHz clock) */
    UART0_IBRD = 13;
    UART0_FBRD = 1;
    /* Set 8-bit word length, enable FIFOs */
    UART0_LCRH = UART_LCRH_WLEN_8BIT | UART_LCRH_FEN;
    /* Enable UART, transmit and receive */
    UART0_CR = UART_CR_UARTEN | UART_CR_TXE | UART_CR_RXE;
#endif
}

/*
 * Send a single character via UART
 */
void uart_putc(char c)
{
#ifdef RAJOS_SEMIHOSTING
    /* Semihosting write0 expects null-terminated string at r1 with r0=0x04 */
    char buf[2] = { c, '\0' };
    __asm volatile (
        "mov r0, %0\n"
        "mov r1, %1\n"
        "bkpt 0xAB\n"
        :
        : "r"(4), "r"(buf)
        : "r0", "r1", "memory"
    );
    if (c == '\n') {
        char cr[2] = { '\r', '\0' };
        __asm volatile (
            "mov r0, %0\n"
            "mov r1, %1\n"
            "bkpt 0xAB\n"
            : : "r"(4), "r"(cr) : "r0", "r1", "memory"
        );
    }
#else
    while (UART0_FR & UART_FR_TXFF) { }
    UART0_DR = c;
    if (c == '\n') {
        uart_putc('\r');
    }
#endif
}

/*
 * Send a null-terminated string via UART
 */
void uart_puts(const char *str)
{
    if (!str) return;
    
    while (*str) {
        uart_putc(*str++);
    }
}

/*
 * Simple implementation of integer to string conversion
 * Avoids division for ARM926EJ-S compatibility
 */
static void itoa(int value, char *str, int base)
{
    char *ptr = str;
    
    /* Handle negative numbers for decimal base */
    if (value < 0 && base == 10) {
        *ptr++ = '-';
        value = -value;
    }
    
    /* Simple conversion without division - just handle common cases */
    if (value == 0) {
        *ptr++ = '0';
    } else if (value < 10) {
        *ptr++ = '0' + value;
    } else if (value < 100) {
        /* For 10-99, use lookup table approach */
        static const char tens[] = "0000000000111111111122222222223333333333444444444455555555556666666666777777777788888888889999999999";
        *ptr++ = tens[value];
        *ptr++ = '0' + (value - (tens[value] - '0') * 10);
    } else {
        /* For larger numbers, just show a placeholder */
        *ptr++ = '?';
    }
    
    *ptr = '\0';
}

/*
 * Basic printf implementation
 * Supports: %d (decimal), %x (hex), %s (string), %c (char)
 */
void uart_printf(const char *format, ...)
{
    if (!format) return;
    
    /* Simple variadic argument handling */
    uint32_t *args = ((uint32_t*)&format) + 1;
    int arg_index = 0;
    char buffer[32];
    
    while (*format) {
        if (*format == '%' && *(format + 1)) {
            format++; /* Skip '%' */
            
            switch (*format) {
                case 'd': /* Decimal integer */
                    itoa((int)args[arg_index++], buffer, 10);
                    uart_puts(buffer);
                    break;
                    
                case 'x': /* Hexadecimal integer */
                    itoa((int)args[arg_index++], buffer, 16);
                    uart_puts(buffer);
                    break;
                    
                case 's': /* String */
                    uart_puts((const char*)args[arg_index++]);
                    break;
                    
                case 'c': /* Character */
                    uart_putc((char)args[arg_index++]);
                    break;
                    
                case '%': /* Literal % */
                    uart_putc('%');
                    break;
                    
                default:
                    uart_putc('%');
                    uart_putc(*format);
                    break;
            }
        } else {
            uart_putc(*format);
        }
        format++;
    }
}