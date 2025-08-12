@echo off
REM RajOS Build Script for Windows
REM Alternative to Makefile when make is not available

echo Building RajOS...

REM Check if ARM toolchain is available
where arm-none-eabi-gcc >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: ARM cross-compiler not found!
    echo Please install ARM GNU Toolchain from:
    echo https://developer.arm.com/downloads/-/gnu-rm
    echo.
    echo Or install via MSYS2:
    echo pacman -S mingw-w64-x86_64-arm-none-eabi-gcc
    echo pacman -S mingw-w64-x86_64-arm-none-eabi-newlib
    pause
    exit /b 1
)

REM Create build directory
if not exist build mkdir build
if not exist build\src mkdir build\src
if not exist build\src\kernel mkdir build\src\kernel
if not exist build\src\arch mkdir build\src\arch
if not exist build\src\arch\arm mkdir build\src\arch\arm
if not exist build\src\drivers mkdir build\src\drivers

REM Compiler settings
set CC=arm-none-eabi-gcc
set AS=arm-none-eabi-as
set LD=arm-none-eabi-ld
set OBJCOPY=arm-none-eabi-objcopy
set SIZE=arm-none-eabi-size

set CFLAGS=-mcpu=cortex-m3 -mthumb -mfloat-abi=soft -fno-common -ffunction-sections -fdata-sections -Wall -Wextra -Werror -std=c99 -Os -Isrc/include -Isrc/include/kernel -Isrc/include/arch -Isrc/include/drivers

set ASFLAGS=-mcpu=cortex-m3 -mthumb

set LDFLAGS=-mcpu=cortex-m3 -mthumb -nostdlib -nostartfiles -Wl,--gc-sections -Wl,--print-memory-usage -T linker.ld

echo Assembling startup.s...
%AS% %ASFLAGS% -o build\src\arch\arm\startup.o src\arch\arm\startup.s
if %ERRORLEVEL% neq 0 goto :error

echo Compiling kernel.c...
%CC% %CFLAGS% -c src\kernel\kernel.c -o build\src\kernel\kernel.o
if %ERRORLEVEL% neq 0 goto :error

echo Compiling uart.c...
%CC% %CFLAGS% -c src\drivers\uart.c -o build\src\drivers\uart.o  
if %ERRORLEVEL% neq 0 goto :error

echo Compiling timer.c...
%CC% %CFLAGS% -c src\drivers\timer.c -o build\src\drivers\timer.o
if %ERRORLEVEL% neq 0 goto :error

echo Compiling task.c...
%CC% %CFLAGS% -c src\kernel\task.c -o build\src\kernel\task.o
if %ERRORLEVEL% neq 0 goto :error

echo Linking RajOS...
%CC% %LDFLAGS% build\src\arch\arm\startup.o build\src\kernel\kernel.o build\src\drivers\uart.o build\src\drivers\timer.o build\src\kernel\task.o -o build\rajos.elf
if %ERRORLEVEL% neq 0 goto :error

echo Creating binary...
%OBJCOPY% -O binary build\rajos.elf build\rajos.bin
if %ERRORLEVEL% neq 0 goto :error

echo Creating hex file...
%OBJCOPY% -O ihex build\rajos.elf build\rajos.hex
if %ERRORLEVEL% neq 0 goto :error

echo Build complete!
%SIZE% build\rajos.elf

echo.
echo To run with QEMU:
echo qemu-system-arm -M versatilepb -cpu cortex-m3 -kernel build\rajos.elf -nographic -serial stdio
echo.
echo Press any key to exit...
pause >nul
exit /b 0

:error
echo BUILD FAILED!
pause
exit /b 1