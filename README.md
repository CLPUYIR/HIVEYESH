# Hiveesh: The Maximalist Distributed AI Swarm 🐝💻

**Hiveesh** is a "one-liner" plug-and-play software layer that transforms any institutional Windows network (college labs, cyber cafés, office LANs) into a **Distributed AI Supercomputer**. 

By aggregating under-utilized commodity hardware, Hiveesh shards frontier-level models like **Llama-3.1 405B** and **DeepSeek-R1** across the network, prioritizing raw performance and "maximalist" intelligence.

---

## 🚀 The Vision: "Hardware-Agnostic Supercomputing"
Most AI tools focus on running small models on single machines. **Hiveesh** does the opposite. It asks: *"What is the largest possible intelligence this entire room can manifest?"*

It uses a **Maximalist Model Matchmaker** to fit the highest-parameter models available onto your collective cluster capacity ($C_{total}$), sharding them via native Win64 binaries to bypass reboots and complex installations.

---

## 🛠 The 6-Stage Architecture

### 1. The One-Liner Bootstrapper (`Hiveesh-Installer.ps1`)
- **Zero-Friction:** A single PowerShell command sets up a portable, no-install Python environment.
- **Admin-Ready:** Verifies privileges and prepares the `C:\ProgramData\Hiveesh` staging area.

### 2. Dynamic Profiling (`profiler.py` & `benchmarker.py`)
- **Nervous System Mapping:** Real-time detection of CPU features (AVX2/AVX512), RAM, and GPU VRAM.
- **Capacity Formula:** 
  $$C_{total} = \sum_{i=1}^{n} (RAM_{i} + VRAM_{i}) - (2GB \times n)$$
- **Network Sweep:** Measures bandwidth and jitter to map the fastest inter-node tensor transfer paths.

### 3. Human-Centric TUI (`tui_wizard.py`)
- **Creative Interface:** An engaging Terminal UI with beautiful ASCII art.
- **Intent Capture:** Instead of technical jargon, it asks: *"Do you want me to reason with you?"* or *"Do you want me to see for you?"*

### 4. Maximalist Matchmaker (`matchmaker.py`)
- **Intelligence Selection:** Cross-references $C_{total}$ with a frontier model database.
- **Optimization:** Automatically picks the largest model (e.g., 405B over 70B) and the best quantization level to maximize the swarm's IQ.

### 5. Distributed Deployment (In Progress)
- **Native Execution:** Deploys `llama-server.exe` shards to nodes.
- **P2P Sync:** Uses parallel synchronization to push 100GB+ weights across the LAN in minutes.

### 6. The Exit Gateway (In Progress)
- **Unified API:** A central FastAPI router exposes the swarm as a single OpenAI-compatible endpoint.
- **Self-Healing:** Instantly re-allocates shards if a node drops from the network.

---

## ⚡ Quick Start

1. **Clone the Hive:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Hiveesh.git
   cd Hiveesh
   ```

2. **Run the Bootstrapper (as Admin):**
   ```powershell
   .\Hiveesh-Installer.ps1
   ```

3. **Wake the Swarm:**
   ```bash
   python profiler.py
   python tui_wizard.py
   ```

---

## 🛡 Security & Performance
- **Priority:** Processes run at "Above Normal" priority for maximum thread utilization.
- **Privacy:** All inference happens locally on your LAN. No data leaves the room.
- **Compatibility:** Designed for standard Windows 10/11 environments without requiring WSL2 (unless specialized creative nodes are needed).

---

## 🤝 Contributing
Hiveesh is an open-source project. We welcome maximalists, systems engineers, and AI enthusiasts to help us turn every LAN into a supercomputer. 

*License: MIT*
