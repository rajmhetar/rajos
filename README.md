# RajOS - Custom Real-Time Operating System

A custom RTOS built from scratch in C with ARM assembly for embedded systems.

## Target Platform
- ARM Cortex-M (simulated with QEMU initially)

## Key Features
- Preemptive multitasking with priority-based scheduler
- Context switching (ARM assembly)  
- Memory management
- Inter-process communication (semaphores, message queues)
- System timer and interrupts

## Project Structure
```
src/
├── kernel/          # Core kernel functionality
├── arch/arm/        # ARM-specific code (assembly, context switching)
├── drivers/         # Hardware drivers
└── include/         # Header files
    ├── kernel/
    ├── arch/
    └── drivers/
build/               # Build artifacts
```

## Build Requirements
- gcc-arm-none-eabi toolchain
- QEMU for ARM simulation
- Make

## Getting Started
```bash
make clean
make all
make run    # Run with QEMU
```