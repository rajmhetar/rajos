# RajOS Makefile
# Cross-compilation for ARM Cortex-M

# Toolchain
CC = arm-none-eabi-gcc
AS = arm-none-eabi-as
LD = arm-none-eabi-ld
OBJCOPY = arm-none-eabi-objcopy
OBJDUMP = arm-none-eabi-objdump
SIZE = arm-none-eabi-size

# Target CPU (Cortex-M3 for QEMU)
CPU = cortex-m3
ARCH = armv7-m

# Directories
SRC_DIR = src
BUILD_DIR = build
KERNEL_DIR = $(SRC_DIR)/kernel
ARCH_DIR = $(SRC_DIR)/arch/arm
DRIVERS_DIR = $(SRC_DIR)/drivers
INCLUDE_DIR = src/include

# Compiler flags
CFLAGS = -mcpu=$(CPU) -mthumb -mfloat-abi=soft
CFLAGS += -fno-common -ffunction-sections -fdata-sections
CFLAGS += -Wall -Wextra -Werror -std=c99
CFLAGS += -Os -g3
CFLAGS += -I$(INCLUDE_DIR) -I$(INCLUDE_DIR)/kernel -I$(INCLUDE_DIR)/arch -I$(INCLUDE_DIR)/drivers

# Assembler flags  
ASFLAGS = -mcpu=$(CPU) -mthumb -g3

# Linker flags
LDFLAGS = -mcpu=$(CPU) -mthumb -nostdlib -nostartfiles
LDFLAGS += -Wl,--gc-sections -Wl,--print-memory-usage
LDFLAGS += -T linker.ld

# Source files
C_SOURCES = $(wildcard $(KERNEL_DIR)/*.c) $(wildcard $(DRIVERS_DIR)/*.c)
ASM_SOURCES = $(wildcard $(ARCH_DIR)/*.s)

# Object files
C_OBJECTS = $(C_SOURCES:%.c=$(BUILD_DIR)/%.o)
ASM_OBJECTS = $(ASM_SOURCES:%.s=$(BUILD_DIR)/%.o)
OBJECTS = $(C_OBJECTS) $(ASM_OBJECTS)

# Output files
TARGET = rajos
ELF = $(BUILD_DIR)/$(TARGET).elf
BIN = $(BUILD_DIR)/$(TARGET).bin
HEX = $(BUILD_DIR)/$(TARGET).hex

# Default target
all: $(ELF) $(BIN) $(HEX)
	@echo "Build complete!"
	@$(SIZE) $(ELF)

# Create ELF file
$(ELF): $(OBJECTS) linker.ld
	@echo "Linking $@"
	@mkdir -p $(dir $@)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

# Create binary file  
$(BIN): $(ELF)
	@echo "Creating binary $@"
	$(OBJCOPY) -O binary $< $@

# Create hex file
$(HEX): $(ELF)
	@echo "Creating hex $@"
	$(OBJCOPY) -O ihex $< $@

# Compile C source files
$(BUILD_DIR)/%.o: %.c
	@echo "Compiling $<"
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

# Assemble ASM source files
$(BUILD_DIR)/%.o: %.s
	@echo "Assembling $<"
	@mkdir -p $(dir $@)
	$(AS) $(ASFLAGS) -c $< -o $@

# Run with QEMU
run: $(BIN)
	@echo "Running RajOS in QEMU..."
	qemu-system-arm -M versatilepb -cpu $(CPU) -kernel $(ELF) -nographic -serial stdio

# Debug with QEMU + GDB
debug: $(ELF)
	@echo "Starting QEMU with GDB server..."
	qemu-system-arm -M versatilepb -cpu $(CPU) -kernel $(ELF) -nographic -serial stdio -s -S &
	@echo "Connect with: arm-none-eabi-gdb $(ELF) -ex 'target remote :1234'"

# Disassemble 
disasm: $(ELF)
	$(OBJDUMP) -D $< > $(BUILD_DIR)/$(TARGET).dis
	@echo "Disassembly saved to $(BUILD_DIR)/$(TARGET).dis"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(BUILD_DIR)

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Dependencies
-include $(OBJECTS:.o=.d)

.PHONY: all clean run debug disasm