# RajOS Hardware Porting Guide

## Current Status
RajOS is designed for ARM926 (QEMU versatilepb) and can be ported to real hardware.

## Recommended Hardware Platforms

### 1. STM32F4 Discovery Board (Recommended)
- **CPU**: ARM Cortex-M4 @ 168MHz
- **Flash**: 1MB
- **RAM**: 192KB
- **Price**: ~$25
- **Why**: Similar to current architecture, excellent tooling

### 2. TI MSP432 LaunchPad
- **CPU**: ARM Cortex-M4F @ 48MHz
- **Flash**: 256KB
- **RAM**: 64KB
- **Price**: ~$20
- **Why**: Good for learning, TI ecosystem

### 3. TI MSPM0 LaunchPad (Your Suggestion)
- **CPU**: ARM Cortex-M0+ @ 80MHz
- **Flash**: 128KB
- **RAM**: 32KB
- **Price**: ~$15
- **Why**: Lowest cost, but requires more porting work

## Porting Requirements

### Memory Layout Changes
Update `linker.ld` for target hardware:
```ld
/* Example for STM32F4 */
MEMORY
{
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 1024K
    RAM (rwx)  : ORIGIN = 0x20000000, LENGTH = 192K
}
```

### Peripheral Drivers
Replace QEMU-specific drivers:
- UART registers and initialization
- Timer/SysTick configuration
- GPIO for LED indicators

### Startup Code
Modify `startup.s` for Cortex-M:
- Cortex-M vector table format
- Cortex-M specific initialization
- Different interrupt handling

## Testing Strategy

### Phase 1: QEMU Testing (Current)
```bash
python build.py    # Build RajOS
python run.py      # Test in QEMU
```

### Phase 2: Hardware Bringup
1. LED blink test (basic I/O)
2. UART output test (console)
3. Timer interrupt test (heartbeat)
4. Task creation test (memory management)
5. Full RTOS test (task switching)

### Phase 3: Real-Time Testing
1. Interrupt latency measurement
2. Context switch timing
3. Memory usage profiling
4. Performance benchmarks

## Flashing to Hardware

### STM32 (ST-Link)
```bash
# Using OpenOCD
openocd -f board/stm32f4discovery.cfg -c "program build/rajos.elf verify reset exit"

# Using st-flash
st-flash write build/rajos.bin 0x08000000
```

### TI Hardware (Uniflash)
```bash
# Using TI Uniflash tool
uniflash.sh -ccxml target.ccxml -program build/rajos.hex
```

## Next Steps for Hardware Port

1. **Choose target board** (STM32F4 Discovery recommended)
2. **Create hardware abstraction layer** (HAL)
3. **Port drivers one by one** (UART first, then timer)
4. **Test incrementally** (bootloader → console → timer → tasks)
5. **Optimize for real-time performance**

## Development Tools

### Debugging
- **QEMU + GDB**: Virtual debugging
- **ST-Link + GDB**: Hardware debugging
- **Serial console**: Printf debugging

### Measurement
- **Logic analyzer**: Timing analysis
- **Oscilloscope**: Interrupt response
- **Profiling tools**: Performance analysis
