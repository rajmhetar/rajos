#!/usr/bin/env python3
"""
RajOS Simple Demo Script
A clean, simple demonstration of RajOS capabilities
"""

import subprocess
import sys
import shutil
from pathlib import Path

class RajOSDemo:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        
    def print_header(self):
        """Print demo header"""
        print("=" * 60)
        print("RajOS - Custom Real-Time Operating System")
        print("=" * 60)
        print("This demonstration shows:")
        print("• Building a custom RTOS from source")
        print("• Running it in QEMU ARM emulator")
        print("• Demonstrating embedded systems development")
        print("=" * 60)
        print()
    
    def check_prerequisites(self):
        """Check if required tools are available"""
        print("🔍 Checking prerequisites...")
        
        # Check ARM toolchain
        if not shutil.which("arm-none-eabi-gcc"):
            print("ERROR: ARM GNU Toolchain not found!")
            print("   Please install from: https://developer.arm.com/downloads/-/gnu-rm")
            return False
        
        # Check QEMU
        qemu_found = False
        qemu_paths = [
            "qemu-system-arm",
            "C:\\Program Files\\qemu\\qemu-system-arm.exe"
        ]
        
        for qemu_path in qemu_paths:
            if shutil.which(qemu_path) or Path(qemu_path).exists():
                qemu_found = True
                self.qemu_cmd = qemu_path
                break
        
        if not qemu_found:
            print("ERROR: QEMU not found!")
            print("   Please install from: https://www.qemu.org/download/")
            return False
        
        print("SUCCESS: All prerequisites found")
        return True
    
    def build_rajos(self):
        """Build RajOS"""
        print("\nBuilding RajOS...")
        print("-" * 40)
        
        # Clean previous build
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        # Run build script
        result = subprocess.run([sys.executable, "build.py"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("ERROR: Build failed!")
            print(result.stderr)
            return False
        
        print("SUCCESS: Build completed successfully!")
        return True
    
    def show_build_info(self):
        """Show information about the build"""
        print("\nBuild Information:")
        print("-" * 40)
        
        # Check if ELF file exists
        elf_file = self.build_dir / "rajos.elf"
        if elf_file.exists():
            file_size = elf_file.stat().st_size
            print(f"SUCCESS: ELF file created: {elf_file}")
            print(f"   Size: {file_size:,} bytes")
        else:
            print("ERROR: ELF file not found!")
            return False
        
        # Check other build artifacts
        bin_file = self.build_dir / "rajos.bin"
        hex_file = self.build_dir / "rajos.hex"
        
        if bin_file.exists():
            print(f"SUCCESS: Binary file: {bin_file}")
        if hex_file.exists():
            print(f"SUCCESS: Hex file: {hex_file}")
        
        return True
    
    def run_demo(self):
        """Run the RajOS demo"""
        print("\nLaunching RajOS in QEMU...")
        print("-" * 40)
        print("RajOS will now run in the QEMU ARM emulator.")
        print("Note: Using versatileab machine for stability (ARM926EJ-S)")
        print("You should see the system boot and start running.")
        print()
        print("Press Ctrl+C to exit QEMU")
        print("-" * 40)
        
        try:
            # Use versatileab machine type for stability (ARM926EJ-S)
            cmd = [
                self.qemu_cmd,
                "-M", "versatileab",
                "-cpu", "arm926",
                "-kernel", str(self.build_dir / "rajos.elf"),
                "-nographic"
            ]
            
            print(f"QEMU command: {' '.join(cmd)}")
            print()
            print("Note: Using versatileab machine type for stability")
            print("This requires ARM926 compatibility mode")
            print()
            
            subprocess.run(cmd)
            
        except KeyboardInterrupt:
            print("\n\nDemo terminated by user")
        except Exception as e:
            print(f"\nERROR: Demo failed: {e}")
            return False
        
        return True
    
    def show_next_steps(self):
        """Show what can be done next"""
        print("\nNext Steps & Extensions")
        print("-" * 40)
        print("Immediate Improvements:")
        print("   • Implement full context switching")
        print("   • Add priority-based task scheduler")
        print("   • Implement semaphores and message queues")
        print()
        print("Advanced Features:")
        print("   • Port to real ARM hardware (STM32F4)")
        print("   • Add file system support")
        print("   • Implement network stack")
        print()
        print("Development Tools:")
        print("   • Debug with GDB: python run.py debug")
        print("   • View disassembly: make disasm")
        print("   • Clean build: python build.py clean")
        print()
    
    def run_full_demo(self):
        """Run the complete demonstration"""
        self.print_header()
        
        if not self.check_prerequisites():
            return False
        
        if not self.build_rajos():
            return False
        
        if not self.show_build_info():
            return False
        
        print("\n" + "="*60)
        print("READY TO RUN RAJOS")
        print("="*60)
        try:
            user_input = input("Press Enter to launch RajOS in QEMU (or type 'q' to quit): ")
            if user_input.lower() == 'q':
                print("Demo cancelled by user")
                return True
        except (EOFError, KeyboardInterrupt):
            print("\nDemo cancelled by user")
            return True
        
        if not self.run_demo():
            return False
        
        self.show_next_steps()
        return True

def main():
    demo = RajOSDemo()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "help":
            print("RajOS Demo Script")
            print("Usage:")
            print("  python demo.py        # Run full demo")
            print("  python demo.py help   # Show this help")
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Use 'python demo.py help' for usage information")
    else:
        success = demo.run_full_demo()
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()
