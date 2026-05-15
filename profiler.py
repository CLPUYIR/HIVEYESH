import ctypes
import platform
import subprocess
import json
import sys
import os

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

def get_ram_info():
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(stat)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    return {
        "total_gb": round(stat.ullTotalPhys / (1024**3), 2),
        "available_gb": round(stat.ullAvailPhys / (1024**3), 2)
    }

def get_gpu_info():
    """Queries GPU info via WMI to avoid heavy dependencies."""
    try:
        output = subprocess.check_output(
            "wmic path win32_VideoController get Name,AdapterRAM /format:list", 
            shell=True, universal_newlines=True
        )
        gpus = []
        current_gpu = {}
        for line in output.splitlines():
            if "Name=" in line:
                current_gpu["name"] = line.split("=")[1].strip()
            if "AdapterRAM=" in line:
                try:
                    ram_bytes = int(line.split("=")[1].strip())
                    current_gpu["vram_gb"] = round(ram_bytes / (1024**3), 2)
                except:
                    current_gpu["vram_gb"] = 0.0
                gpus.append(current_gpu)
                current_gpu = {}
        return gpus if gpus else [{"name": "Generic/Integrated", "vram_gb": 0.0}]
    except:
        return [{"name": "Unknown", "vram_gb": 0.0}]

def check_cpu_feature(feature_id):
    # PF_AVX2_INSTRUCTIONS_AVAILABLE = 40, PF_AVX512F_INSTRUCTIONS_AVAILABLE = 41
    return ctypes.windll.kernel32.IsProcessorFeaturePresent(feature_id) != 0

def profile_node():
    ram = get_ram_info()
    gpus = get_gpu_info()
    total_vram = sum(g["vram_gb"] for g in gpus)
    
    # Capacity Calculation: (RAM + VRAM) - 2GB buffer
    capacity = round((ram["available_gb"] + total_vram) - 2.0, 2)
    if capacity < 0: capacity = 0.0

    data = {
        "node": platform.node(),
        "cpu": {
            "cores": os.cpu_count(),
            "avx2": check_cpu_feature(40),
            "avx512": check_cpu_feature(41)
        },
        "ram": ram,
        "gpus": gpus,
        "net_capacity_gb": capacity
    }
    
    with open("node_profile.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return data

if __name__ == "__main__":
    print("--- Hyveyesh Stage 2: Dynamic Profiler ---")
    node_data = profile_node()
    print(f"Node: {node_data['node']}")
    print(f"Cluster Contribution: {node_data['net_capacity_gb']} GB")
    print(f"GPU(s): {', '.join(g['name'] for g in node_data['gpus'])}")
