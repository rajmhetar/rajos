# RajOS - Custom Real-Time Operating System

A custom RTOS built from scratch in C with ARM assembly for embedded systems.

## Quick Start

### **Interactive GUI (Recommended)**
```bash
python run_gui.py
```

This launches a modern GUI that:
- **Visualizes** RajOS architecture
- **Builds** RajOS with one click
- **Tests** different QEMU configurations
- **Monitors** real-time system output
- **Configures** build settings

### **Simple Demo**
```bash
python demo.py
```

This will:
1. Check prerequisites (ARM toolchain, QEMU)
2. Build RajOS from source
3. Show build information
4. Launch RajOS in QEMU ARM emulator

### **Manual Build & Run**
```bash
# Build RajOS
python build.py

# Run in QEMU
python run.py

# Clean build
python build.py clean
```

## What This Demonstrates

- **Custom RTOS Development** - Building an operating system from scratch
- **ARM Architecture** - Cross-compilation and ARM assembly integration
- **Embedded Systems** - Real-time operating system concepts
- **Hardware Abstraction** - Driver development and hardware simulation

## Prerequisites

- **Python 3.7+** with **tkinter** (usually included)
- **ARM GNU Toolchain** - [Download here](https://developer.arm.com/downloads/-/gnu-rm)
- **QEMU** - [Download here](https://www.qemu.org/download/)

## Project Structure

```
rajos/
├── src/
│   ├── kernel/          # Core RTOS functionality
│   ├── arch/arm/        # ARM-specific assembly code
│   ├── drivers/         # Hardware drivers (UART, Timer)
│   └── include/         # Header files
├── rajos_gui.py         # Interactive GUI application
├── run_gui.py           # GUI launcher
├── demo.py              # Demo launcher
├── build.py             # Build script
└── run.py               # Run script
```

## Key Features

- **Task Management** - Task Control Blocks and scheduling
- **Memory Management** - Stack allocation and memory layout
- **Hardware Drivers** - UART console and system timer
- **ARM Integration** - Vector table and exception handling
- **Interactive GUI** - Visual OS showcase and testing interface


## Next Steps

After launching the GUI or running the demo, explore:
1. **Code Structure** - Examine the source files
2. **Architecture** - Understand the design patterns
3. **Extensions** - Add new features and drivers
4. **Hardware** - Port to real ARM boards

