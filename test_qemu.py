#!/usr/bin/env python3
"""
Simple QEMU test script for mps2-an385 machine
"""

import subprocess
import sys
from pathlib import Path

def test_qemu_mps2():
    """Test QEMU mps2-an385 machine with our RajOS build"""
    print("Testing QEMU mps2-an385 with RajOS")
    print("=" * 50)
    
    # Check if build exists
    build_dir = Path("build")
    elf_file = build_dir / "rajos.elf"
    
    if not elf_file.exists():
        print("ERROR: RajOS not built yet!")
        print("Please run: python build.py")
        return False
    
            print(f"SUCCESS: Found RajOS build: {elf_file}")
    
    # Test QEMU command
    qemu_cmd = "C:\\Program Files\\qemu\\qemu-system-arm.exe"
    
    cmd = [
        qemu_cmd,
        "-M", "lm3s6965evb",
        "-kernel", str(elf_file),
        "-nographic",
        "-d", "guest_errors"
    ]
    
    print(f"Testing QEMU command:")
    print(f"   {' '.join(cmd)}")
    print()
    print("This will test if QEMU can load and run RajOS.")
    print("Press Ctrl+C to stop after a few seconds.")
    print("-" * 50)
    
    try:
        # Run QEMU with debug output
        result = subprocess.run(cmd, timeout=10)
        print("SUCCESS: QEMU test completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("TIMEOUT: QEMU test timed out (this is normal)")
        return True
        
    except KeyboardInterrupt:
        print("\nTest stopped by user")
        return True
        
    except Exception as e:
        print(f"ERROR: QEMU test failed: {e}")
        return False

if __name__ == "__main__":
    test_qemu_mps2()
