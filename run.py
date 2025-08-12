#!/usr/bin/env python3
"""
RajOS Run Script
Launch RajOS in QEMU for testing
Author: Raj Mhetar
"""

import subprocess
import sys
import shutil
from pathlib import Path

def check_qemu():
    """Check if QEMU is available"""
    qemu_paths = [
        "qemu-system-arm",  # Standard path
        "C:\\Program Files\\qemu\\qemu-system-arm.exe"  # Windows path
    ]
    
    for qemu_path in qemu_paths:
        if shutil.which(qemu_path) or Path(qemu_path).exists():
            return qemu_path
    
    return None

def run_rajos():
    """Run RajOS in QEMU"""
    print("RajOS QEMU Test Runner")
    print("=" * 30)
    
    # Check if build exists
    elf_file = Path("build/rajos.elf")
    if not elf_file.exists():
        print("ERROR: rajos.elf not found!")
        print("Please build first using: python build.py")
        return False
    
    # Check QEMU
    qemu_cmd = check_qemu()
    if not qemu_cmd:
        print("ERROR: QEMU not found!")
        print("Please install QEMU from: https://www.qemu.org/download/")
        return False
    
    print(f"Using QEMU: {qemu_cmd}")
    print(f"Running: {elf_file}")
    print()
    print("Expected output:")
    print("- RajOS initialization messages")
    print("- Kernel banner")
    print("- Timer ticks every second")
    print("- Kernel heartbeat messages")
    print()
    print("Press Ctrl+C to exit")
    print("-" * 30)
    
    # Run QEMU
    try:
        cmd = [
            qemu_cmd,
            "-M", "versatilepb",
            "-cpu", "arm926",
            "-kernel", str(elf_file),
            "-nographic"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\nQEMU terminated by user")
    except Exception as e:
        print(f"ERROR: Failed to run QEMU: {e}")
        return False
    
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print("RajOS Test Runner")
        print("Usage:")
        print("  python run.py       # Run RajOS in QEMU")
        print("  python run.py help  # Show this help")
    else:
        run_rajos()

if __name__ == "__main__":
    main()
