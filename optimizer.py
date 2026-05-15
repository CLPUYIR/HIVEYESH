import psutil
import os
import sys

def set_high_priority():
    """Sets the current process to 'Above Normal' priority."""
    try:
        p = psutil.Process(os.getpid())
        # ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
        if sys.platform == 'win32':
            p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            print("Process priority set to ABOVE_NORMAL")
        else:
            p.nice(-10) # Unix equivalent
            print("Process priority set to high (-10)")
    except Exception as e:
        print(f"Failed to set priority: {e}")

if __name__ == "__main__":
    # Since psutil might not be there, we can also use a pure-ctypes version for Windows
    import ctypes
    
    def set_priority_win32():
        # SetPriorityClass(GetCurrentProcess(), ABOVE_NORMAL_PRIORITY_CLASS)
        # ABOVE_NORMAL_PRIORITY_CLASS = 0x8000
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        if ctypes.windll.kernel32.SetPriorityClass(handle, 0x8000):
            print("Native Win32: Process priority set to ABOVE_NORMAL")
        else:
            print("Native Win32: Failed to set priority")

    set_priority_win32()
