# RajOS Setup Instructions

## Required Tools

To build and run RajOS, you need:

1. **ARM GNU Toolchain** (cross-compiler for ARM Cortex-M)
2. **QEMU** (for ARM system emulation)
3. **Make** (optional, we provide build.bat for Windows)

## Windows Installation

### Option 1: ARM GNU Toolchain (Recommended)
1. Download from: https://developer.arm.com/downloads/-/gnu-rm
2. Install to default location (usually `C:\Program Files (x86)\GNU Arm Embedded Toolchain`)
3. Add to PATH: `C:\Program Files (x86)\GNU Arm Embedded Toolchain\bin`

### Option 2: MSYS2 (Alternative)
```bash
# Install MSYS2 from https://www.msys2.org/
# Then in MSYS2 terminal:
pacman -S mingw-w64-x86_64-arm-none-eabi-gcc
pacman -S mingw-w64-x86_64-arm-none-eabi-newlib
pacman -S mingw-w64-x86_64-qemu
```

### Install QEMU
1. Download from: https://www.qemu.org/download/
2. Or via MSYS2: `pacman -S mingw-w64-x86_64-qemu`

## Building RajOS

### Using build.bat (Windows)
```cmd
build.bat
```

### Using Makefile (if make available)
```bash
make clean
make all
```

## Running RajOS

### With QEMU
```bash
# Windows
qemu-system-arm -M versatilepb -cpu cortex-m3 -kernel build/rajos.elf -nographic -serial stdio

# Or use the Makefile
make run
```

### Expected Output
```
Initializing RajOS kernel...
UART driver initialized
Kernel initialization complete

========================================
         RajOS v0.1.0
  Custom Real-Time Operating System
     Built from scratch in C/ARM
========================================

RajOS is now running!
System ready for multitasking...

Kernel heartbeat: 0
Kernel heartbeat: 1
...
```

## Troubleshooting

### "arm-none-eabi-gcc not found"
- Ensure ARM toolchain is installed and in PATH
- Restart terminal/command prompt after installation

### "QEMU not found"
- Install QEMU and add to PATH
- Or use full path to qemu-system-arm

### Build errors
- Check all source files are present in src/ directories
- Verify toolchain versions are compatible
- Try clean build: delete build/ directory and rebuild

## Next Steps

Once basic kernel boots successfully:
1. Add system timer (SysTick)
2. Implement task switching
3. Add memory management
4. Build scheduler
5. Add IPC mechanisms