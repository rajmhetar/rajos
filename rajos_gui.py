#!/usr/bin/env python3
"""
RajOS GUI - Interactive Operating System Showcase and Testing Interface
A modern GUI application that demonstrates RajOS architecture and provides testing capabilities
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import queue
import os
import sys
from datetime import datetime
import json

class RajOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RajOS - Real-Time Operating System Showcase")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Output queue for thread-safe updates
        self.output_queue = queue.Queue()
        
        # Current process
        self.current_process = None
        self.is_running = False
        
        self.setup_styles()
        self.create_widgets()
        self.setup_output_monitor()
        
    def setup_styles(self):
        """Configure modern styling for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground='#00ff88',
                       background='#2b2b2b')
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#00ccff',
                       background='#2b2b2b')
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#ffffff',
                       background='#2b2b2b')
        
        style.configure('Success.TButton',
                       background='#00ff88',
                       foreground='#000000')
        
        style.configure('Danger.TButton',
                       background='#ff4444',
                       foreground='#ffffff')
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="RajOS - Real-Time Operating System",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Overview tab
        self.create_overview_tab(notebook)
        
        # Architecture tab
        self.create_architecture_tab(notebook)
        
        # Testing tab
        self.create_testing_tab(notebook)
        
        # Build tab
        self.create_build_tab(notebook)
        
        # Output tab
        self.create_output_tab(notebook)
        
    def create_overview_tab(self, notebook):
        """Create the overview tab with RajOS introduction"""
        overview_frame = ttk.Frame(notebook)
        notebook.add(overview_frame, text="Overview")
        
        # Introduction
        intro_text = """
RajOS is a custom real-time operating system built from scratch in C and ARM assembly.

Key Features:
• Real-time task scheduling with priorities
• Preemptive multitasking
• Memory management (simple heap)
• Hardware abstraction layer
• ARM Cortex-M3/ARM926EJ-S support
• UART and timer drivers
• Exception handling and interrupt system

Target Platforms:
• QEMU emulation (versatileab, mps2-an385)
• STM32F4 microcontrollers
• TI MSP432 and MSPM0
• Any ARM Cortex-M compatible device

Perfect For:
• Learning OS development
• Embedded systems education
• Real-time applications
• ARM architecture understanding
        """
        
        intro_label = tk.Label(overview_frame, 
                              text=intro_text,
                              font=('Consolas', 10),
                              fg='#00ff88',
                              bg='#1e1e1e',
                              justify=tk.LEFT,
                              padx=20,
                              pady=20)
        intro_label.pack(fill=tk.BOTH, expand=True)
        
    def create_architecture_tab(self, notebook):
        """Create the architecture tab showing system design"""
        arch_frame = ttk.Frame(notebook)
        notebook.add(arch_frame, text="Architecture")
        
        # Create canvas for architecture diagram
        canvas = tk.Canvas(arch_frame, bg='#1e1e1e', height=600)
        canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Draw architecture diagram
        self.draw_architecture_diagram(canvas)
        
    def draw_architecture_diagram(self, canvas):
        """Draw the RajOS architecture diagram"""
        # Colors
        colors = {
            'kernel': '#00ff88',
            'drivers': '#00ccff',
            'hardware': '#ff8800',
            'text': '#ffffff'
        }
        
        # Kernel layer
        canvas.create_rectangle(50, 50, 350, 150, 
                              fill=colors['kernel'], outline='#ffffff', width=2)
        canvas.create_text(200, 100, text="RajOS Kernel", 
                          font=('Segoe UI', 14, 'bold'), fill='#000000')
        
        # Task management
        canvas.create_rectangle(50, 170, 150, 220, 
                              fill=colors['kernel'], outline='#ffffff', width=2)
        canvas.create_text(100, 195, text="Task\nManager", 
                          font=('Segoe UI', 10, 'bold'), fill='#000000')
        
        # Memory management
        canvas.create_rectangle(160, 170, 260, 220, 
                              fill=colors['kernel'], outline='#ffffff', width=2)
        canvas.create_text(210, 195, text="Memory\nManager", 
                          font=('Segoe UI', 10, 'bold'), fill='#000000')
        
        # Scheduler
        canvas.create_rectangle(270, 170, 370, 220, 
                              fill=colors['kernel'], outline='#ffffff', width=2)
        canvas.create_text(320, 195, text="Scheduler", 
                          font=('Segoe UI', 10, 'bold'), fill='#000000')
        
        # Drivers layer
        canvas.create_rectangle(50, 250, 350, 320, 
                              fill=colors['drivers'], outline='#ffffff', width=2)
        canvas.create_text(200, 285, text="Hardware Drivers", 
                          font=('Segoe UI', 12, 'bold'), fill='#000000')
        
        # UART driver
        canvas.create_rectangle(50, 330, 150, 380, 
                              fill=colors['drivers'], outline='#ffffff', width=2)
        canvas.create_text(100, 355, text="UART\nDriver", 
                          font=('Segoe UI', 10, 'bold'), fill='#000000')
        
        # Timer driver
        canvas.create_rectangle(160, 330, 260, 380, 
                              fill=colors['drivers'], outline='#ffffff', width=2)
        canvas.create_text(210, 355, text="Timer\nDriver", 
                          font=('Segoe UI', 10, 'bold'), fill='#000000')
        
        # Hardware layer
        canvas.create_rectangle(50, 400, 350, 480, 
                              fill=colors['hardware'], outline='#ffffff', width=2)
        canvas.create_text(200, 440, text="Hardware Layer", 
                          font=('Segoe UI', 12, 'bold'), fill='#000000')
        
        # ARM CPU
        canvas.create_oval(100, 410, 150, 460, 
                          fill=colors['hardware'], outline='#ffffff', width=2)
        canvas.create_text(125, 435, text="ARM\nCPU", 
                          font=('Segoe UI', 8, 'bold'), fill='#000000')
        
        # Memory
        canvas.create_oval(200, 410, 250, 460, 
                          fill=colors['hardware'], outline='#ffffff', width=2)
        canvas.create_text(225, 435, text="RAM/\nFlash", 
                          font=('Segoe UI', 8, 'bold'), fill='#000000')
        
        # Peripherals
        canvas.create_oval(300, 410, 350, 460, 
                          fill=colors['hardware'], outline='#ffffff', width=2)
        canvas.create_text(325, 435, text="UART/\nTimer", 
                          font=('Segoe UI', 8, 'bold'), fill='#000000')
        
        # Arrows
        canvas.create_line(200, 150, 200, 250, fill=colors['text'], width=2, arrow=tk.LAST)
        canvas.create_line(200, 320, 200, 400, fill=colors['text'], width=2, arrow=tk.LAST)
        
    def create_testing_tab(self, notebook):
        """Create the testing tab for running and testing RajOS"""
        test_frame = ttk.Frame(notebook)
        notebook.add(test_frame, text="Testing")
        
        # Testing controls
        controls_frame = tk.Frame(test_frame, bg='#2b2b2b')
        controls_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Build button
        self.build_btn = ttk.Button(controls_frame, 
                                                                       text="Build RajOS",
                                   command=self.build_rajos,
                                   style='Success.TButton')
        self.build_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Run button
        self.run_btn = ttk.Button(controls_frame, 
                                                                   text="Run in QEMU",
                                 command=self.run_rajos,
                                 state=tk.DISABLED)
        self.run_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(controls_frame, 
                                                                     text="Stop QEMU",
                                  command=self.stop_rajos,
                                  state=tk.DISABLED,
                                  style='Danger.TButton')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear output button
        clear_btn = ttk.Button(controls_frame, 
                                                             text="Clear Output",
                              command=self.clear_output)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status frame
        status_frame = tk.Frame(test_frame, bg='#2b2b2b')
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Status label
        self.status_label = ttk.Label(status_frame, 
                                     text="Status: Ready",
                                     style='Info.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, 
                                       mode='indeterminate',
                                       length=200)
        self.progress.pack(side=tk.RIGHT)
        
        # Testing options
        options_frame = tk.LabelFrame(test_frame, 
                                     text="Testing Options",
                                     bg='#2b2b2b',
                                     fg='#ffffff',
                                     font=('Segoe UI', 10, 'bold'))
        options_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # QEMU machine selection
        machine_frame = tk.Frame(options_frame, bg='#2b2b2b')
        machine_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(machine_frame, 
                 text="QEMU Machine:",
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        self.machine_var = tk.StringVar(value="versatileab")
        machine_combo = ttk.Combobox(machine_frame, 
                                    textvariable=self.machine_var,
                                    values=["versatileab", "mps2-an385", "lm3s6965evb"],
                                    state="readonly",
                                    width=15)
        machine_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # CPU selection
        cpu_frame = tk.Frame(options_frame, bg='#2b2b2b')
        cpu_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(cpu_frame, 
                 text="CPU Type:",
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        self.cpu_var = tk.StringVar(value="arm926")
        cpu_combo = ttk.Combobox(cpu_frame, 
                                 textvariable=self.cpu_var,
                                 values=["arm926", "cortex-m3"],
                                 state="readonly",
                                 width=15)
        cpu_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Output mode
        output_frame = tk.Frame(options_frame, bg='#2b2b2b')
        output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(output_frame, 
                 text="Output Mode:",
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        self.output_mode = tk.StringVar(value="console")
        output_combo = ttk.Combobox(output_frame, 
                                   textvariable=self.output_mode,
                                   values=["console", "file", "gui"],
                                   state="readonly",
                                   width=15)
        output_combo.pack(side=tk.LEFT, padx=(10, 0))
        
    def create_build_tab(self, notebook):
        """Create the build tab showing build configuration and process"""
        build_frame = ttk.Frame(notebook)
        notebook.add(build_frame, text="Build")
        
        # Build configuration
        config_frame = tk.LabelFrame(build_frame, 
                                    text="Build Configuration",
                                    bg='#2b2b2b',
                                    fg='#ffffff',
                                    font=('Segoe UI', 10, 'bold'))
        config_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Compiler settings
        compiler_frame = tk.Frame(config_frame, bg='#2b2b2b')
        compiler_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(compiler_frame, 
                 text="Compiler:",
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        self.compiler_var = tk.StringVar(value="arm-none-eabi-gcc")
        compiler_entry = ttk.Entry(compiler_frame, 
                                  textvariable=self.compiler_var,
                                  width=30)
        compiler_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Build flags
        flags_frame = tk.Frame(config_frame, bg='#2b2b2b')
        flags_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(flags_frame, 
                 text="CFLAGS:",
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        self.cflags_var = tk.StringVar(value="-mcpu=arm926ej-s -marm -O2 -g")
        cflags_entry = ttk.Entry(flags_frame, 
                                textvariable=self.cflags_var,
                                width=50)
        cflags_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Linker script
        linker_frame = tk.Frame(config_frame, bg='#2b2b2b')
        linker_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(linker_frame, 
                 text="Linker Script:",
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        self.linker_var = tk.StringVar(value="linker.ld")
        linker_entry = ttk.Entry(linker_frame, 
                                textvariable=self.linker_var,
                                width=30)
        linker_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Build info
        info_frame = tk.LabelFrame(build_frame, 
                                  text="Build Information",
                                  bg='#2b2b2b',
                                  fg='#ffffff',
                                  font=('Segoe UI', 10, 'bold'))
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Build info text
        self.build_info_text = scrolledtext.ScrolledText(info_frame,
                                                        bg='#1e1e1e',
                                                        fg='#00ff88',
                                                        font=('Consolas', 9),
                                                        height=15)
        self.build_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Populate build info
        self.populate_build_info()
        
    def create_output_tab(self, notebook):
        """Create the output tab for displaying system output"""
        output_frame = ttk.Frame(notebook)
        notebook.add(output_frame, text="Output")
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(output_frame,
                                                    bg='#1e1e1e',
                                                    fg='#00ff88',
                                                    font=('Consolas', 10),
                                                    height=30)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Output controls
        output_controls = tk.Frame(output_frame, bg='#2b2b2b')
        output_controls.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Save output button
        save_btn = ttk.Button(output_controls, 
                                                           text="Save Output",
                             command=self.save_output)
        save_btn.pack(side=tk.LEFT)
        
        # Load output button
        load_btn = ttk.Button(output_controls, 
                                                           text="Load Output",
                             command=self.load_output)
        load_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Timestamp toggle
        self.timestamp_var = tk.BooleanVar(value=True)
        timestamp_check = ttk.Checkbutton(output_controls,
                                         text="Show Timestamps",
                                         variable=self.timestamp_var,
                                         style='Info.TLabel')
        timestamp_check.pack(side=tk.RIGHT)
        
    def setup_output_monitor(self):
        """Set up the output monitor thread"""
        def monitor_output():
            while True:
                try:
                    message = self.output_queue.get(timeout=0.1)
                    self.output_text.insert(tk.END, message + "\n")
                    self.output_text.see(tk.END)
                    self.output_queue.task_done()
                except queue.Empty:
                    continue
                    
        self.output_thread = threading.Thread(target=monitor_output, daemon=True)
        self.output_thread.start()
        
    def log_output(self, message):
        """Add timestamped message to output queue"""
        if self.timestamp_var.get():
            timestamp = datetime.now().strftime("%H:%M:%S")
            message = f"[{timestamp}] {message}"
        self.output_queue.put(message)
        
    def build_rajos(self):
        """Build RajOS using the build system"""
        self.log_output("Starting RajOS build...")
        self.build_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Status: Building...")
        
        def build_thread():
            try:
                # Check if build.py exists
                if not os.path.exists("build.py"):
                    self.log_output("ERROR: build.py not found!")
                    return
                
                # Run build
                result = subprocess.run([sys.executable, "build.py"], 
                                      capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    self.log_output("SUCCESS: Build completed successfully!")
                    self.log_output(f"Build output:\n{result.stdout}")
                    self.run_btn.config(state=tk.NORMAL)
                else:
                    self.log_output(f"ERROR: Build failed with return code {result.returncode}")
                    self.log_output(f"Build errors:\n{result.stderr}")
                    
            except subprocess.TimeoutExpired:
                self.log_output("TIMEOUT: Build timed out after 60 seconds")
            except Exception as e:
                self.log_output(f"ERROR: Build error: {str(e)}")
            finally:
                self.root.after(0, self.build_finished)
                
        threading.Thread(target=build_thread, daemon=True).start()
        
    def build_finished(self):
        """Called when build process finishes"""
        self.build_btn.config(state=tk.NORMAL)
        self.progress.stop()
        self.status_label.config(text="Status: Build finished")
        
    def run_rajos(self):
        """Run RajOS in QEMU"""
        self.log_output("Starting RajOS in QEMU...")
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        self.status_label.config(text="Status: Running...")
        self.is_running = True
        
        def run_thread():
            try:
                # Build QEMU command
                qemu_cmd = [
                    "qemu-system-arm",
                    "-M", self.machine_var.get(),
                    "-cpu", self.cpu_var.get(),
                    "-kernel", "build/rajos.elf",
                    "-nographic"
                ]
                
                if self.output_mode.get() == "file":
                    qemu_cmd.extend(["-serial", "file:rajos_output.txt"])
                elif self.output_mode.get() == "gui":
                    qemu_cmd.remove("-nographic")
                
                self.log_output(f"QEMU command: {' '.join(qemu_cmd)}")
                
                # Start QEMU
                self.current_process = subprocess.Popen(
                    qemu_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Monitor output
                while self.is_running and self.current_process.poll() is None:
                    output = self.current_process.stdout.readline()
                    if output:
                        self.log_output(f"QEMU: {output.strip()}")
                    error = self.current_process.stderr.readline()
                    if error:
                        self.log_output(f"QEMU Error: {error.strip()}")
                        
            except Exception as e:
                self.log_output(f"ERROR: Run error: {str(e)}")
            finally:
                self.root.after(0, self.run_finished)
                
        threading.Thread(target=run_thread, daemon=True).start()
        
    def stop_rajos(self):
        """Stop the running QEMU process"""
        if self.current_process:
            self.log_output("Stopping QEMU...")
            self.is_running = False
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            self.current_process = None
            
        self.run_finished()
        
    def run_finished(self):
        """Called when run process finishes"""
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        self.status_label.config(text="Status: Ready")
        self.is_running = False
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
        self.log_output("Output cleared")
        
    def save_output(self):
        """Save output to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.output_text.get(1.0, tk.END))
                self.log_output(f"SUCCESS: Output saved to {filename}")
            except Exception as e:
                self.log_output(f"ERROR: Error saving output: {str(e)}")
                
    def load_output(self):
        """Load output from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, content)
                self.log_output(f"SUCCESS: Output loaded from {filename}")
            except Exception as e:
                self.log_output(f"ERROR: Error loading output: {str(e)}")
                
    def populate_build_info(self):
        """Populate build information display"""
        info = """RajOS Build Configuration
=======================

Target Architecture: ARM926EJ-S
Compiler: arm-none-eabi-gcc
Build System: Python + Makefile

Source Files:
• src/kernel/kernel.c - Main kernel entry point
• src/kernel/task.c - Task management system
• src/arch/arm/startup.s - ARM startup code
• src/drivers/uart.c - UART driver
• src/drivers/timer.c - Timer driver

Build Process:
1. Compile C sources with ARM cross-compiler
2. Assemble ARM startup code
3. Link with custom linker script
4. Generate ELF binary for QEMU

Key Features:
• Real-time task scheduling
• Memory management
• Hardware abstraction
• Exception handling
• Interrupt system

QEMU Compatibility:
• Machine: versatileab (ARM926EJ-S)
• CPU: arm926
• Output: Console, file, or GUI
        """
        
        self.build_info_text.delete(1.0, tk.END)
        self.build_info_text.insert(1.0, info)

def main():
    """Main entry point"""
    root = tk.Tk()
    app = RajOSGUI(root)
    
    # Set window icon if available
    try:
        root.iconbitmap('rajos.ico')
    except:
        pass
        
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
