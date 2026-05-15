# 🐝 HYVEYESH: THE ULTIMATE ARCHITECTURAL BLUEPRINT (v1.0)

> **"A Maximalist Distributed AI Swarm for Windows Networks."**  
> This document serves as the absolute source of truth for the Hyveyesh project. It contains the technical logic, architectural separation, and the 6-stage execution pipeline required to rebuild or extend the swarm.

---

## 1. IDENTITY & VISION
*   **Project Name:** Hyveyesh (formerly Hiveesh).
*   **Core Mandate:** Transform institutional Windows LANs into a single Distributed Supercomputer.
*   **Philosophy:** "Maximalist Intelligence." Prioritize the **Largest Possible Model** (e.g., Llama-3.1 405B) over inference speed or quantization precision.
*   **Target Environment:** Heterogeneous Windows 10/11 networks (College labs, Office LANs, Cyber Cafés).

---

## 2. THE MAXIMALIST FORMULA ($C_{total}$)
Hyveyesh calculates the collective cluster capacity to determine model sharding feasibility:
$$C_{total} = \sum_{i=1}^{n} (RAM_{available, i} + VRAM_{available, i}) - (2GB \times n)$$
*   **Buffer:** 2GB per node is reserved for OS stability.
*   **Recycling:** Aggregates CPU-RAM and GPU-VRAM into a unified virtual memory pool.

---

## 3. ARCHITECTURAL SEPARATION (PLANE LOGIC)
To bypass Windows' inherent protocol latencies, Hyveyesh splits all operations into two distinct planes:

### A. The Management Plane (The "Construction Workers")
*   **Protocols:** WinRM (SOAP/XML), Robocopy (SMB).
*   **Purpose:** Installation, firewall configuration, registry tweaks, and static model weight distribution.
*   **Tooling:** PowerShell (`Hyveyesh-Installer.ps1`, `Hyveyesh-Deploy.ps1`).

### B. The Data Plane (The "Neural Path")
*   **Protocol:** Raw Binary over Persistent TCP Sockets (llama.cpp RPC backend).
*   **Purpose:** Real-time transfer of Neural Network activations (tensors).
*   **Execution:** Native Win64 `llama-server.exe` running in `--rpc` mode.
*   **Optimization:** Bypasses the Windows OS management stack; talks directly to the Network Interface Card (NIC) via C-level sockets.

---

## 4. THE 6-STAGE EXECUTION PIPELINE

### STAGE 1: THE INCUBATION (`Hyveyesh-Installer.ps1`)
*   **Action:** One-liner bootstrapper.
*   **Logic:** Verifies Admin rights -> Deploys Portable Win64 Python -> Sets up `C:\ProgramData\Hyveyesh`.
*   **Bypass:** No-install, no-reboot architecture.

### STAGE 2: NERVOUS SYSTEM MAPPING (`profiler.py` & `benchmarker.py`)
*   **Action:** HW/NW Diagnostics.
*   **HW Profiler:** Detects AVX2/AVX512, RAM, and GPU VRAM via native Win32/WMI calls.
*   **NW Benchmarker:** Measures Jitter and Throughput to map the "Fastest Neural Path."

### STAGE 3: THE AWAKENING (`tui_wizard.py`)
*   **Action:** Human-Centric Command Center.
*   **UX:** Interactive ASCII-based TUI. Captures user intent (Reasoning, Vision, Creative) via natural language questions.

### STAGE 4: THE MATCHMAKER (`matchmaker.py`)
*   **Action:** Intelligence Selection.
*   **Logic:** Cross-references $C_{total}$ from Stage 2 with User Intent from Stage 3.
*   **Priority:** Selects the largest parameter-count model available (e.g., 405B over 70B) and calculates the optimal 4-bit/6-bit quantization.

### STAGE 5: SHARD DISTRIBUTION (`distributor.py`)
*   **Action:** Parallel Weight Sync & Remote Execution.
*   **Sync:** Uses `robocopy /MT:32 /Z` to push sharded weights from Master to Workers.
*   **Execution:** Remote-triggers `llama-server.exe --rpc` on all nodes via WinRM.
*   **Feasibility:** Only sharded layers are cached in local RAM (e.g., 8GB per PC for a 230GB model).

### STAGE 6: THE EXIT GATEWAY (`gateway.py`)
*   **Action:** Unified Inference & Self-Healing.
*   **API:** Central FastAPI router providing an OpenAI-compatible endpoint.
*   **Self-Healing:** Background monitor detects node failure -> Triggers emergency re-sharding -> Resumes inference queue.

---

## 5. TECHNICAL DEEP-DIVE (FOR AI PARSING)

### Sharding & KV Cache
*   **Weight Sharding:** Static weights stay in node RAM.
*   **KV Cache:** Locally sharded. Node A stores the cache for its specific layers.
*   **Activations:** Only the output tensor (Activations) moves across the network (Unicast).
*   **Latency:** Network travel time is minimized by raw TCP stream; roughly 10-30ms per node hop on Gigabit LAN.

### Performance Optimization (`optimizer.py`)
*   **Process Priority:** All worker threads are set to `ABOVE_NORMAL_PRIORITY_CLASS` (0x8000) using native Win32 `SetPriorityClass`.
*   **Thread Utilization:** Workers utilize `os.cpu_count()` to saturate all available logic cores.

---

## 6. RECOVERY & TROUBLESHOOTING
*   **Protocol Wall:** If WinRM times out, the system defaults to "Direct Execution" if the node is already bootstrapped.
*   **Memory Pressure:** If RAM is exceeded, the Matchmaker automatically drops to a lower quantization (e.g., Q4_K_S) before failing.
*   **Network Jitter:** High-jitter nodes are de-prioritized in the "Neural Path" to prevent bottlenecking the entire swarm.

---

## 7. PROJECT METRICS (FOR GPT/LLM CONTEXT)
*   **Language:** Python 3.11 (Embedded), PowerShell 5.1+.
*   **Inference Engine:** llama.cpp (Win64 Native).
*   **Registry Tweaks:** `LongPathsEnabled = 1`.
*   **Firewall Rules:** Inbound TCP 8000-8100.

---

**DOCUMENT END.**  
*This blueprint is the source of truth for Hyveyesh. Any AI or developer reading this possesses the full logic to instantiate, repair, or evolve the swarm.* 🐝🚀
