/*
 * RajOS Linker Script
 * ARM926EJ-S Memory Layout
 */

/* Memory layout for QEMU versatileab (ARM926EJ-S) */
MEMORY
{
    /* Flash memory - where code and constants are stored */
    /* For ARM926 (QEMU versatileab), flash typically starts at 0x00000000 */
    FLASH (rx) : ORIGIN = 0x00000000, LENGTH = 256K
    
    /* RAM - for variables, stack, and heap */
    RAM (rwx)  : ORIGIN = 0x20000000, LENGTH = 64K
}

/* Stack size (grows downward from top of RAM) */
_stack_size = 0x1000; /* 4KB stack */

/* Entry point */
ENTRY(Reset_Handler)

SECTIONS
{
    /* Vector table - must be at the start of flash */
    .vectors :
    {
        . = ALIGN(4);
        KEEP(*(.vectors))
        . = ALIGN(4);
    } > FLASH
    
    /* Program code and read-only data */
    .text :
    {
        . = ALIGN(4);
        *(.text)           /* Program code */
        *(.text*)
        *(.rodata)         /* Read-only data */
        *(.rodata*)
        
        . = ALIGN(4);
        _etext = .;        /* End of code section */
    } > FLASH
    
    /* Exception handling frame info */
    .eh_frame :
    {
        *(.eh_frame)
    } > FLASH
    
    /* Initialized data - copied from flash to RAM at startup */
    .data : AT(_etext)
    {
        . = ALIGN(4);
        _data_start = .;   /* Start of data in RAM */
        *(.data)
        *(.data*)
        . = ALIGN(4);
        _data_end = .;     /* End of data in RAM */
    } > RAM
    
    _data_load_start = LOADADDR(.data); /* Data location in flash */
    _data_size = _data_end - _data_start;
    
    /* Uninitialized data - zeroed at startup */
    .bss :
    {
        . = ALIGN(4);
        _bss_start = .;
        *(.bss)
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        _bss_end = .;
    } > RAM
    
    _bss_size = _bss_end - _bss_start;
    
    /* Heap starts after BSS */
    . = ALIGN(8);
    _heap_start = .;
    
    /* Stack at top of RAM (grows downward) */
    _stack_top = ORIGIN(RAM) + LENGTH(RAM);
    _stack_bottom = _stack_top - _stack_size;
    _heap_end = _stack_bottom;
    
    /* Make sure we don't exceed RAM */
    ASSERT(_heap_start < _heap_end, "Not enough RAM for heap and stack")
    
    /* Debug sections (not loaded) */
    .comment 0 : { *(.comment) }
    .debug_info 0 : { *(.debug_info) }
    .debug_abbrev 0 : { *(.debug_abbrev) }
    .debug_line 0 : { *(.debug_line) }
    .debug_frame 0 : { *(.debug_frame) }
    .debug_str 0 : { *(.debug_str) }
    .debug_ranges 0 : { *(.debug_ranges) }
}