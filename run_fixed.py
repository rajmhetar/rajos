#!/usr/bin/env python3
"""
RajOS Fixed Runner
Working QEMU configuration for Windows
Author: Raj Mhetar
"""

import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

def check_qemu():
    """Check if QEMU is available"""
    qemu_paths = [
        "qemu-system-arm",
        "C:\\Program Files\\qemu\\qemu-system-arm.exe"
    ]
    
    for qemu_path in qemu_paths:
        if shutil.which(qemu_path) or Path(qemu_path).exists():
            return qemu_path
    return None

def run_rajos_windows():
    """Run RajOS with Windows-compatible QEMU settings"""
    print("RajOS Windows Test Runner")
    print("=" * 40)
    
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
        return False
    
    print(f"Using QEMU: {qemu_cmd}")
    print(f"Running: {elf_file}")
    print()
    
    # Try different approaches
    approaches = [
        {
            "name": "Method 1: TCP Serial Output",
            "cmd": [qemu_cmd, "-M", "versatilepb", "-cpu", "arm926", 
                   "-kernel", str(elf_file), "-nographic", 
                   "-serial", "tcp:127.0.0.1:1234,server,nowait"],
            "note": "Connect with: telnet 127.0.0.1 1234"
        },
        {
            "name": "Method 2: File Output", 
            "cmd": [qemu_cmd, "-M", "versatilepb", "-cpu", "arm926",
                   "-kernel", str(elf_file), "-nographic",
                   "-serial", "file:rajos_output.txt"],
            "note": "Output will be in rajos_output.txt"
        },
        {
            "name": "Method 3: Monitor Only",
            "cmd": [qemu_cmd, "-M", "versatilepb", "-cpu", "arm926",
                   "-kernel", str(elf_file), "-nographic"],
            "note": "QEMU monitor - type 'info registers' to see if CPU is running"
        }
    ]
    
    for i, approach in enumerate(approaches, 1):
        print(f"\n{approach['name']}")
        print(f"Note: {approach['note']}")
        print("Command:", " ".join(approach['cmd']))
        
        response = input(f"Try method {i}? (y/n/q): ").lower()
        
        if response == 'q':
            break
        elif response == 'y':
            try:
                print("Starting QEMU... Press Ctrl+C to stop")
                print("-" * 40)
                
                if "file:" in " ".join(approach['cmd']):
                    # For file output, run for 10 seconds then show file
                    process = subprocess.Popen(approach['cmd'])
                    import time
                    time.sleep(10)
                    process.terminate()
                    
                    # Show file content
                    output_file = Path("rajos_output.txt")
                    if output_file.exists():
                        print("RajOS Output:")
                        print(output_file.read_text())
                    else:
                        print("No output file created")
                        
                else:
                    # For other methods, run interactively
                    subprocess.run(approach['cmd'])
                    
            except KeyboardInterrupt:
                print("\nStopped by user")
            except Exception as e:
                print(f"Error: {e}")
        
        print("-" * 40)
    
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print("RajOS Windows Runner")
        print("Tries different methods to get QEMU output on Windows")
    else:
        run_rajos_windows()

if __name__ == "__main__":
    main()
