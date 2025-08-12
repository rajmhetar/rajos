@echo off
echo ========================================
echo         RajOS Test Script
echo ========================================
echo.

echo Checking required tools...
echo.

REM Check ARM toolchain
echo [1/3] Checking ARM cross-compiler...
where arm-none-eabi-gcc >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✓ ARM toolchain found
    arm-none-eabi-gcc --version | findstr "arm-none-eabi-gcc"
) else (
    echo ✗ ARM toolchain NOT found!
    echo Please install from: https://developer.arm.com/downloads/-/gnu-rm
    echo.
    pause
    exit /b 1
)

echo.

REM Check QEMU
echo [2/3] Checking QEMU...
where qemu-system-arm >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✓ QEMU found
    qemu-system-arm --version | findstr "QEMU"
) else (
    echo ✗ QEMU NOT found!
    echo Please install from: https://www.qemu.org/download/
    echo.
    pause
    exit /b 1
)

echo.

REM Build RajOS
echo [3/3] Building RajOS...
echo.
call build.bat
if %ERRORLEVEL% neq 0 (
    echo.
    echo ✗ Build failed! Check errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo         Build Successful!
echo ========================================
echo.
echo To run RajOS in QEMU, use:
echo   qemu-system-arm -M versatilepb -cpu cortex-m3 -kernel build/rajos.elf -nographic -serial stdio
echo.
echo Or simply run: test-run.bat
echo.
pause 