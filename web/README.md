# Interactive Web-Based Digital Logic Circuit Simulator

## 🌐 Overview

This is a companion web-based EDA (Electronic Design Automation) module for the **Digital Logic Circuit Simulator** project (Advanced Data Structures and Algorithms).

It allows users to visually **drag-and-drop logic gates, draw interconnect wires, toggle input switches, view live signal propagation, and generate truth tables** in an interactive HTML5 Canvas environment.

---

## 🔗 Synchronization with the C++ Module

The web module is synchronized with the C++ code in two ways:

1. **Algorithm Parity ([`circuit-engine.js`](circuit-engine.js)):**
   - Implements the exact same graph data structures and algorithms as `Circuit.h`, `Gate.h`, `UnionFind.h`, and `Simulator.h`.
   - **Tarjan's 3-Colour DFS** (`hasCycleDFS`): Detects feedback loops and highlights them in glowing red.
   - **Kahn's BFS Topological Sort** (`topologicalSort`): Resolves dependency execution order and animates gates step-by-step.
   - **Gate Boolean Evaluation** (`evaluateGate`): Exact evaluation for all 9 gate types (INPUT, OUTPUT, AND, OR, NOT, XOR, NAND, NOR, XNOR).
   - **Exhaustive Truth Table Generator** (`generateTruthTableJS`): Tests all $2^N$ input combinations via bitwise operations.

2. **C++ Code Generator & Bridge ([`server.py`](server.py)):**
   - Click **"⚙️ Export C++ Code"** in the web UI to generate the exact C++ function (`buildExportedCircuit()`) matching `Circuit.h`!
   - Run `python server.py` to start the local backend server, which can invoke `simulator.exe` on demand for native C++ execution.

---

## 🚀 How to Run the Web Simulator

### Method 1: Instant Standalone (No Server Required!)
Simply double-click [`index.html`](index.html) or open it in any web browser (Chrome, Edge, Firefox, Brave):
```powershell
Start-Process "c:\Projects\DigitalLogicSimulator\web\index.html"
```

### Method 2: With Local Python Server
```powershell
cd c:\Projects\DigitalLogicSimulator\web
python server.py
```
This serves the application on `http://localhost:8000` and automatically launches your browser.

---

## 🎮 Features & Controls

- **Drag & Drop Gates:** Drag any gate from the left palette onto the canvas.
- **Draw Wires:** Click and drag from any gate's **Right Port (Output)** to another gate's **Left Port (Input)**.
- **Live Signal Glow:**
  - 🟢 **Green Glowing Wire:** Signal is `1 (HIGH)`
  - ⚪ **Slate Gray Wire:** Signal is `0 (LOW)`
- **Interactive INPUT Switches:** Click on any INPUT switch on the canvas to toggle its value between `0` and `1` in real time.
- **Live OUTPUT Bulbs:** The bulb indicator glows bright gold when the signal is `1`.
- **Topological Step Animation:** Click **"🔄 Step-by-Step Topo"** to watch Kahn's algorithm evaluate gates in sequence!
- **Exhaustive Truth Table:** Click **"📊 Truth Table"** to compute and view all $2^N$ truth table rows.
- **Preset Circuits:** Load **Half Adder**, **NOR Circuit**, **2-to-1 Multiplexer**, or the **IEEE ISCAS '85 c17 Benchmark** with a single click.
- **Delete Gate:** Click to select a gate (blue border) and press **Delete** or **Backspace**.
