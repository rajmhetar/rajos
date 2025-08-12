@echo off
echo ========================================
echo         Running RajOS in QEMU
echo ========================================
echo.

REM Check if binary exists
if not exist "build\rajos.elf" (
    echo ✗ RajOS binary not found!
    echo Please build first using: test.bat
    echo.
    pause
    exit /b 1
)

echo Starting QEMU with RajOS...
echo.
echo Expected output:
echo - RajOS initialization messages
echo - Kernel banner
echo - Heartbeat messages every few seconds
echo.
echo Press Ctrl+C to exit QEMU
echo.

REM Run RajOS in QEMU
qemu-system-arm -M versatilepb -cpu cortex-m3 -kernel build/rajos.elf -nographic -serial stdio

echo.
echo QEMU exited.
pause 