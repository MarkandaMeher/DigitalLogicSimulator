# Digital Logic Circuit Simulator

> **Course**: Advanced Data Structures & Algorithms  
> **Authors**: Markanda Meher (Roll No. 206126020) & Nikhil (Roll No. 206126021)  
> **Date**: October 2026 (First Review)

An end-to-end software framework for constructing, validating, and simulating digital combinational circuits. This project demonstrates the practical application of fundamental graph algorithms and data structures to eliminate physical hardware prototyping constraints (breadboard wire clutter, loose pins, burnt IC chips, and lack of automated error checking).

---

## 🚀 Key Features

* **Directed Graph Circuit Engine (C++17)**: High-performance core modeling logic gates as vertices and directional wires as edges.
* **Automated Cycle Detection**: Traps illegal feedback loops and back-edges using **Tarjan's 3-Color DFS** prior to simulation.
* **Topological Evaluation Scheduling**: Determines exact race-free calculation order using **Kahn's In-Degree Queue Algorithm** ($O(V + E)$).
* **Automated $2^N$ Truth Table Verification**: Generates exhaustive truth tables across all binary permutations in milliseconds.
* **Interactive Drag-and-Drop Web GUI (`web/`)**: Canvas-based EDA editor with glowing live wires (Green = HIGH, Gray = LOW), interactive input switches, and animated topological sorting.
* **IEEE ISCAS '85 Benchmark Validation**: Built-in verification against industry-standard CAD benchmark circuits (specifically `c17`: 6 NAND gates, 5 inputs, 2 outputs).

---

## 🧠 Core Algorithms & Data Structures

| Module | Data Structure / Algorithm | Time Complexity | Space Complexity | Purpose |
|---|---|:---:|:---:|---|
| **Circuit Netlist** | Adjacency List + Hash Map | $O(V + E)$ | $O(V + E)$ | $O(1)$ gate lookup by ID; sparse graph representation |
| **Cycle Trapping** | Tarjan's 3-Color DFS | $O(V + E)$ | $O(V)$ | Traps back-edges (feedback loops) with White/Gray/Black node coloration |
| **Eval Scheduling** | Kahn's In-Degree BFS | $O(V + E)$ | $O(V)$ | Establishes dependency-safe linear execution order |
| **Logic Simulation** | Topological Boolean Dispatch | $O(V + E)$ | $O(V)$ | Evaluates gates level-by-level (AND, OR, NOT, XOR, NAND, NOR, XNOR) |
| **Truth Table** | Bitwise Iteration ($2^N$ states) | $O(2^N \cdot (V + E))$ | $O(V)$ | Exhaustive verification against theoretical Boolean algebra |
| **Wire Netting** | Disjoint-Set Union (DSU) | $O(m \cdot \alpha(n))$ | $O(V)$ | Equipotential wire net grouping with path compression & union by rank |

---

## 📂 Project Structure

```text
DigitalLogicSimulator/
├── Circuit.h               # Directed Graph (DAG) netlist representation & topology
├── Gate.h                  # Gate structures, pins, and Boolean logic dispatch
├── Simulator.h              # DFS cycle detector, Kahn's topo sort & truth table engine
├── UnionFind.h              # Disjoint-Set Union with path compression & union by rank
├── main.cpp                # Interactive C++ CLI menu, ASCII schematics & demos
├── simulator.exe           # Pre-compiled standalone static executable (Windows)
│
├── web/                    # Interactive Drag-and-Drop Web EDA Canvas
│   ├── index.html          # Clean web editor interface
│   ├── style.css           # Modern dark UI theme with glowing wire styling
│   ├── circuit-engine.js   # 1:1 JS implementation of C++ graph algorithms
│   ├── app.js              # HTML5 Canvas controller & Kahn's animation
│   └── server.py           # Local HTTP server & C++ simulation bridge
│
├── Digital_Logic_Simulator_First_Review_Academic_V2.pptx # 12-slide clean review PPT
├── First_Review_Academic_V2.pdf                          # 12-slide review PDF
├── Project_Mastery_Guide.pdf                             # Comprehensive study & viva PDF
└── README.md
```

---

## 🛠️ How to Run

### 1. C++ Console Simulator
Run the pre-compiled standalone binary:
```powershell
.\simulator.exe
```
Or compile from source using any C++17 compiler:
```bash
g++ -std=c++17 -O2 -static -o simulator.exe main.cpp
.\simulator.exe
```
* **Interactive Demos Available**:
  * Option `8`: Half Adder (`Sum = A XOR B`, `Carry = A AND B`)
  * Option `9`: NOR Gate (`Y = NOT(A OR B)`)
  * Option `10`: 2-to-1 Multiplexer (`Y = (A AND NOT S) OR (B AND S)`)
  * Option `11`: Official **IEEE ISCAS '85 c17 Benchmark** (32 truth table rows)
  * Option `12`: Cycle detection test circuit (trapping intentional feedback loops)

### 2. Interactive Web Drag-and-Drop GUI
Open [`web/index.html`](web/index.html) directly in any web browser, or launch the local server:
```bash
python web/server.py
```
* Drag gates from the palette onto the canvas.
* Connect output pins to input pins.
* Click input switches to toggle signals live (wires glow green when HIGH).
* Click **"Animate Kahn's Algo"** to watch topological sorting step-by-step.
* Click **"Truth Table"** to generate the full state table.

---

## 📚 Review Deliverables & Documentation

* **First Review Presentation (PPTX)**: [`Digital_Logic_Simulator_First_Review_Academic_V2.pptx`](Digital_Logic_Simulator_First_Review_Academic_V2.pptx)
* **First Review Presentation (PDF)**: [`First_Review_Academic_V2.pdf`](First_Review_Academic_V2.pdf)
* **Project Mastery & Viva Guide (PDF)**: [`Project_Mastery_Guide.pdf`](Project_Mastery_Guide.pdf)
* **Full Technical Report (PDF)**: [`Digital_Logic_Circuit_Simulator_Project_Report.pdf`](Digital_Logic_Circuit_Simulator_Project_Report.pdf)
