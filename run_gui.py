#!/usr/bin/env python3
"""
RajOS GUI Launcher
Simple script to launch the RajOS GUI application
"""

import sys
import os

def main():
    """Launch the RajOS GUI"""
    print("Launching RajOS GUI...")
    
    # Check if tkinter is available
    try:
        import tkinter
        print("SUCCESS: Tkinter is available")
    except ImportError:
        print("ERROR: Tkinter is not available")
        print("Please install tkinter or use a Python distribution that includes it")
        return 1
    
    # Check if the GUI file exists
    if not os.path.exists("rajos_gui.py"):
        print("ERROR: rajos_gui.py not found")
        print("Please make sure you're in the correct directory")
        return 1
    
    # Launch the GUI
    try:
        print("Starting RajOS GUI...")
        import rajos_gui
        rajos_gui.main()
        return 0
    except Exception as e:
        print(f"ERROR: Error launching GUI: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
