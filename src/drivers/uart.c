/*
 * RajOS UART Driver
 * Basic UART driver for console output on QEMU versatilepb
 */

#include "drivers/uart.h"

/* UART0 registers for QEMU versatilepb */
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

/*
 * Initialize UART0 for basic console output
 */
void uart_init(void)
{
    /* Disable UART */
    UART0_CR = 0;
    
    /* Set baud rate to 115200 (assuming 24MHz clock) */
    /* Integer part: 24000000 / (16 * 115200) = 13.02 -> 13 */
    /* Fractional part: 0.02 * 64 = 1.28 -> 1 */
    UART0_IBRD = 13;
    UART0_FBRD = 1;
    
    /* Set 8-bit word length, enable FIFOs */
    UART0_LCRH = UART_LCRH_WLEN_8BIT | UART_LCRH_FEN;
    
    /* Enable UART, transmit and receive */
    UART0_CR = UART_CR_UARTEN | UART_CR_TXE | UART_CR_RXE;
}

/*
 * Send a single character via UART
 */
void uart_putc(char c)
{
    /* Wait until transmit FIFO is not full */
    while (UART0_FR & UART_FR_TXFF) {
        /* Busy wait */
    }
    
    /* Send character */
    UART0_DR = c;
    
    /* Convert LF to CRLF for proper terminal display */
    if (c == '\n') {
        uart_putc('\r');
    }
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
 */
static void itoa(int value, char *str, int base)
{
    char *ptr = str;
    char *ptr1 = str;
    char tmp_char;
    int tmp_value;
    
    /* Handle negative numbers for decimal base */
    if (value < 0 && base == 10) {
        *ptr++ = '-';
        value = -value;
        ptr1++;
    }
    
    /* Convert to string (reverse order) */
    do {
        tmp_value = value;
        value /= base;
        *ptr++ = "0123456789abcdef"[tmp_value - value * base];
    } while (value);
    
    *ptr-- = '\0';
    
    /* Reverse string */
    while (ptr1 < ptr) {
        tmp_char = *ptr;
        *ptr-- = *ptr1;
        *ptr1++ = tmp_char;
    }
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