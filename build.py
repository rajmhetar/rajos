#!/usr/bin/env python3
"""
RajOS Build Script
Cross-platform build system for RajOS RTOS
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class RajOSBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.src_dir = self.project_root / "src"
        
        # Toolchain commands
        self.cc = "arm-none-eabi-gcc"
        self.as_cmd = "arm-none-eabi-as"
        self.ld = "arm-none-eabi-ld"
        self.objcopy = "arm-none-eabi-objcopy"
        self.size = "arm-none-eabi-size"
        
        # Compiler flags
        self.cflags = [
            "-mcpu=arm926ej-s",
            "-marm",
            "-mfloat-abi=soft",
            "-fno-common",
            "-ffunction-sections",
            "-fdata-sections",
            "-Wall",
            "-Wextra",
            "-std=c99",
            "-Os",
            "-DRAJOS_SEMIHOSTING"
        ]
        
        self.include_dirs = [
            str(self.src_dir / "include"),
            str(self.src_dir / "include" / "kernel"),
            str(self.src_dir / "include" / "arch"),
            str(self.src_dir / "include" / "drivers")
        ]
        
        self.asflags = ["-mcpu=arm926ej-s"]
        self.ldflags = [
            "-mcpu=arm926ej-s",
            "-marm",
            "-nostdlib",
            "-nostartfiles",
            "-Wl,--gc-sections",
            "-Wl,--print-memory-usage",
            "-T", "linker.ld"
        ]
        
        # Source files
        self.c_sources = [
            self.src_dir / "kernel" / "kernel.c",
            self.src_dir / "drivers" / "uart.c",
            self.src_dir / "drivers" / "timer.c",
            self.src_dir / "kernel" / "task.c"
        ]
        
        self.asm_sources = [
            self.src_dir / "arch" / "arm" / "startup.s"
        ]
        
        # Output files
        self.target = "rajos"
        self.elf_file = self.build_dir / f"{self.target}.elf"
        self.bin_file = self.build_dir / f"{self.target}.bin"
        self.hex_file = self.build_dir / f"{self.target}.hex"

    def check_toolchain(self):
        """Check if ARM toolchain is available"""
        print("Checking ARM toolchain...")
        
        tools = [self.cc, self.as_cmd, self.ld, self.objcopy, self.size]
        missing_tools = []
        
        for tool in tools:
            if shutil.which(tool) is None:
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"ERROR: Missing tools: {', '.join(missing_tools)}")
            print("Please install ARM GNU Toolchain from:")
            print("https://developer.arm.com/downloads/-/gnu-rm")
            return False
        
        print("ARM toolchain found")
        return True

    def create_build_dirs(self):
        """Create build directory structure"""
        print("Creating build directories...")
        
        dirs_to_create = [
            self.build_dir,
            self.build_dir / "src" / "kernel",
            self.build_dir / "src" / "drivers",
            self.build_dir / "src" / "arch" / "arm"
        ]
        
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print("Build directories created")

    def compile_c_file(self, source_file):
        """Compile a C source file"""
        # Create the correct object file path
        relative_path = source_file.relative_to(self.src_dir)
        obj_file = self.build_dir / relative_path.with_suffix('.o')
        
        # Ensure the object file directory exists
        obj_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [self.cc] + self.cflags + ["-c", str(source_file), "-o", str(obj_file)]
        
        for include_dir in self.include_dirs:
            cmd.extend(["-I", include_dir])
        
        print(f"Compiling {source_file.name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"ERROR: Compilation failed for {source_file.name}:")
            print(result.stderr)
            return None
        
        print(f"Compiled {source_file.name}")
        return obj_file

    def compile_asm_file(self, source_file):
        """Compile an assembly source file"""
        # Create the correct object file path
        relative_path = source_file.relative_to(self.src_dir)
        obj_file = self.build_dir / relative_path.with_suffix('.o')
        
        # Ensure the object file directory exists
        obj_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [self.as_cmd] + self.asflags + ["-c", str(source_file), "-o", str(obj_file)]
        
        print(f"Assembling {source_file.name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"ERROR: Assembly failed for {source_file.name}:")
            print(result.stderr)
            return None
        
        print(f"Assembled {source_file.name}")
        return obj_file

    def link(self, object_files):
        """Link object files into ELF"""
        print("Linking RajOS...")
        
        cmd = [self.cc] + self.ldflags + [str(obj) for obj in object_files] + ["-o", str(self.elf_file)]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("ERROR: Linking failed:")
            print(result.stderr)
            return False
        
        print("Linking completed")
        return True

    def create_binary_files(self):
        """Create binary and hex files"""
        print("Creating binary files...")
        
        # Create binary file
        cmd = [self.objcopy, "-O", "binary", str(self.elf_file), str(self.bin_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("ERROR: Binary creation failed:")
            print(result.stderr)
            return False
        
        # Create hex file
        cmd = [self.objcopy, "-O", "ihex", str(self.elf_file), str(self.hex_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("ERROR: Hex file creation failed:")
            print(result.stderr)
            return False
        
        print("Binary files created")
        return True

    def show_build_info(self):
        """Show build information"""
        if self.elf_file.exists():
            result = subprocess.run([self.size, str(self.elf_file)], capture_output=True, text=True)
            if result.returncode == 0:
                print("\nBuild Information:")
                print(result.stdout)
        
        print(f"\nOutput files:")
        print(f"   ELF: {self.elf_file}")
        print(f"   BIN: {self.bin_file}")
        print(f"   HEX: {self.hex_file}")

    def build(self):
        """Main build process"""
        print("Building RajOS...")
        print("=" * 50)
        
        # Check toolchain
        if not self.check_toolchain():
            return False
        
        # Create build directories
        self.create_build_dirs()
        
        # Compile all source files
        object_files = []
        
        # Compile C files
        for c_file in self.c_sources:
            if c_file.exists():
                obj_file = self.compile_c_file(c_file)
                if obj_file:
                    object_files.append(obj_file)
                else:
                    return False
            else:
                print(f"Warning: {c_file} not found")
        
        # Compile assembly files
        for asm_file in self.asm_sources:
            if asm_file.exists():
                obj_file = self.compile_asm_file(asm_file)
                if obj_file:
                    object_files.append(obj_file)
                else:
                    return False
            else:
                print(f"Warning: {asm_file} not found")
        
        if not object_files:
            print("ERROR: No object files created")
            return False
        
        # Link
        if not self.link(object_files):
            return False
        
        # Create binary files
        if not self.create_binary_files():
            return False
        
        # Show build info
        self.show_build_info()
        
        print("\nBuild completed successfully!")
        return True

    def clean(self):
        """Clean build artifacts"""
        print("Cleaning build artifacts...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            print("Build directory cleaned")
        else:
            print("Build directory doesn't exist")

def main():
    builder = RajOSBuilder()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "clean":
            builder.clean()
        elif sys.argv[1] == "help":
            print("RajOS Build Script")
            print("Usage:")
            print("  python build.py        # Build RajOS")
            print("  python build.py clean  # Clean build artifacts")
            print("  python build.py help   # Show this help")
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Use 'python build.py help' for usage information")
    else:
        success = builder.build()
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()
