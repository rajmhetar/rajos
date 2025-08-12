#!/usr/bin/env python3
"""
RajOS Debug Runner
Diagnose QEMU issues and test different configurations
Author: Raj Mhetar
"""

import subprocess
import sys
import shutil
import time
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

def test_qemu_basic():
    """Test basic QEMU functionality"""
    print("Testing QEMU basic functionality...")
    
    qemu_cmd = check_qemu()
    if not qemu_cmd:
        print("ERROR: QEMU not found!")
        return False
    
    # Test QEMU version
    try:
        result = subprocess.run([qemu_cmd, "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"QEMU Version: {result.stdout.strip()}")
            return True
        else:
            print(f"QEMU version check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"QEMU test failed: {e}")
        return False

def test_rajos_different_configs():
    """Try different QEMU configurations"""
    qemu_cmd = check_qemu()
    elf_file = Path("build/rajos.elf")
    
    configs = [
        {
            "name": "Original (versatilepb + arm926)",
            "cmd": [qemu_cmd, "-M", "versatilepb", "-cpu", "arm926", 
                   "-kernel", str(elf_file), "-nographic"]
        },
        {
            "name": "With serial stdio",
            "cmd": [qemu_cmd, "-M", "versatilepb", "-cpu", "arm926", 
                   "-kernel", str(elf_file), "-nographic", "-serial", "stdio"]
        },
        {
            "name": "With monitor stdio",
            "cmd": [qemu_cmd, "-M", "versatilepb", "-cpu", "arm926", 
                   "-kernel", str(elf_file), "-nographic", "-monitor", "stdio"]
        },
        {
            "name": "Verbose output",
            "cmd": [qemu_cmd, "-M", "versatilepb", "-cpu", "arm926", 
                   "-kernel", str(elf_file), "-nographic", "-d", "guest_errors"]
        }
    ]
    
    print("Testing different QEMU configurations...")
    print("Each test will run for 5 seconds")
    print()
    
    for i, config in enumerate(configs, 1):
        print(f"Test {i}: {config['name']}")
        print(f"Command: {' '.join(config['cmd'])}")
        print("Output:")
        print("-" * 40)
        
        try:
            # Run for 5 seconds then kill
            process = subprocess.Popen(config['cmd'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True)
            
            # Wait for 5 seconds
            time.sleep(5)
            
            # Check if there's any output
            try:
                stdout, stderr = process.communicate(timeout=1)
                if stdout:
                    print("STDOUT:")
                    print(stdout)
                if stderr:
                    print("STDERR:")
                    print(stderr)
                    
                if not stdout and not stderr:
                    print("No output detected")
                    
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                print("Process killed after timeout")
                if stdout:
                    print("STDOUT:")
                    print(stdout)
                if stderr:
                    print("STDERR:")
                    print(stderr)
                
        except Exception as e:
            print(f"Test failed: {e}")
        
        print("-" * 40)
        print()

def check_elf_file():
    """Check the ELF file properties"""
    elf_file = Path("build/rajos.elf")
    
    if not elf_file.exists():
        print("ERROR: rajos.elf not found!")
        return False
    
    # Check file size
    file_size = elf_file.stat().st_size
    print(f"ELF file size: {file_size} bytes")
    
    # Try to get ELF info using objdump if available
    try:
        result = subprocess.run(["arm-none-eabi-objdump", "-h", str(elf_file)], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("ELF sections:")
            print(result.stdout)
        else:
            print("Could not analyze ELF file")
    except:
        print("arm-none-eabi-objdump not available")
    
    return True

def main():
    print("RajOS Debug Runner")
    print("=" * 50)
    print()
    
    # Check prerequisites
    print("1. Checking ELF file...")
    if not check_elf_file():
        return
    print()
    
    print("2. Testing QEMU...")
    if not test_qemu_basic():
        return
    print()
    
    print("3. Testing different QEMU configurations...")
    test_rajos_different_configs()
    
    print("Debug complete!")

if __name__ == "__main__":
    main()
