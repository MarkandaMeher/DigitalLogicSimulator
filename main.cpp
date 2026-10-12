// =============================================================
// main.cpp — Digital Logic Circuit Simulator (Interactive CLI v2.0)
// =============================================================
// Enhanced user-friendly interactive interface with:
//   • Visual ASCII Circuit Schematics & Diagrams
//   • Signal Flow Pipeline (Inputs -> Logic -> Outputs)
//   • Step-by-Step Simulation Execution Trace
//   • Individual Gate Inspector & Signal Probing
//   • Complete Truth Table Generator with Output Statistics
//   • Built-in IEEE ISCAS '85 Benchmark c17 Integration
//
// Team: Markanda Meher (Roll No. 206126020) & Nikhil (Roll No. 206126021)
// Course: Advanced Data Structures & Algorithms
// =============================================================

#include "Circuit.h"
#include "Simulator.h"
#include "UnionFind.h"
#include <iostream>
#include <string>
#include <limits>
#include <iomanip>

// ---------------------------------------------------------
// Utility: Clear input buffer after invalid input
// ---------------------------------------------------------
void clearInput() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// ---------------------------------------------------------
// Utility: Read an integer safely from user
// ---------------------------------------------------------
bool readInt(int& value) {
    if (std::cin >> value) {
        return true;
    }
    clearInput();
    return false;
}

// ---------------------------------------------------------
// printMenu: Displays the organized categorized menu
// ---------------------------------------------------------
void printMenu() {
    std::cout << "\n";
    std::cout << "==============================================================\n";
    std::cout << "         DIGITAL LOGIC CIRCUIT SIMULATOR (CLI v2.0)\n";
    std::cout << "   Advanced Data Structures & Algorithms Project Review\n";
    std::cout << "==============================================================\n";
    std::cout << "  --- CIRCUIT CONSTRUCTION ---\n";
    std::cout << "   1. Add Logic Gate (INPUT, OUTPUT, AND, OR, NOT, etc.)\n";
    std::cout << "   2. Connect Gates (Draw Directed Wire)\n";
    std::cout << "   3. Set Primary Input Value (0 or 1)\n\n";

    std::cout << "  --- VISUALIZATION & INSPECTION ---\n";
    std::cout << "   4. View Circuit Topology Table & Wiring Map\n";
    std::cout << "   5. View Signal Flow Pipeline (Inputs -> Logic -> Outputs)\n";
    std::cout << "   6. View ASCII Circuit Schematic Diagram\n";
    std::cout << "   7. Inspect Gate / Wire Probe (Diagnostic View)\n\n";

    std::cout << "  --- ANALYSIS & SIMULATION ---\n";
    std::cout << "   8. Check for Feedback Loops & Cycles (Tarjan's DFS)\n";
    std::cout << "   9. Simulate Circuit (Fast or Step-by-Step with signal flow)\n";
    std::cout << "  10. Generate Exhaustive Truth Table (All 2^N Combinations)\n\n";

    std::cout << "  --- BUILT-IN PRESET BENCHMARK DEMOS ---\n";
    std::cout << "  11. Demo: Half Adder (XOR + AND with schematic)\n";
    std::cout << "  12. Demo: NOR Gate (OR + NOT with schematic)\n";
    std::cout << "  13. Demo: 2-to-1 Multiplexer (3 Inputs, 5 Gates with schematic)\n";
    std::cout << "  14. Demo: IEEE ISCAS '85 c17 Benchmark (6 NANDs, 32 rows)\n\n";

    std::cout << "   0. Exit Simulator\n";
    std::cout << "==============================================================\n";
    std::cout << "  Enter your choice (0-14): ";
}

// ---------------------------------------------------------
// selectGateType: Interactive selector for all 9 gate types
// ---------------------------------------------------------
GateType selectGateType() {
    std::cout << "\n    Available Gate Types:\n";
    std::cout << "      1. INPUT   (Primary circuit input pin)\n";
    std::cout << "      2. OUTPUT  (Primary circuit measurement pin)\n";
    std::cout << "      3. AND     (Outputs 1 only if ALL inputs are 1)\n";
    std::cout << "      4. OR      (Outputs 1 if ANY input is 1)\n";
    std::cout << "      5. NOT     (Inverts single input: 1->0, 0->1)\n";
    std::cout << "      6. XOR     (Outputs 1 if inputs are DIFFERENT)\n";
    std::cout << "      7. NAND    (Inverted AND: universal gate)\n";
    std::cout << "      8. NOR     (Inverted OR: universal gate)\n";
    std::cout << "      9. XNOR    (Inverted XOR: equality detector)\n";
    std::cout << "    Select gate type (1-9): ";

    int typeChoice;
    if (!readInt(typeChoice) || typeChoice < 1 || typeChoice > 9) {
        std::cout << "    [!] Invalid choice. Defaulting to INPUT.\n";
        return GateType::INPUT;
    }

    switch (typeChoice) {
        case 1: return GateType::INPUT;
        case 2: return GateType::OUTPUT;
        case 3: return GateType::AND;
        case 4: return GateType::OR;
        case 5: return GateType::NOT;
        case 6: return GateType::XOR;
        case 7: return GateType::NAND;
        case 8: return GateType::NOR;
        case 9: return GateType::XNOR;
        default: return GateType::INPUT;
    }
}

// ---------------------------------------------------------
// listGatesCompact: Compact summary list of all gates
// ---------------------------------------------------------
void listGatesCompact(const Circuit& circuit) {
    if (circuit.gates.empty()) {
        std::cout << "    (No gates exist currently)\n";
        return;
    }
    std::cout << "    Current Gates in Circuit:\n";
    for (const auto& gate : circuit.gates) {
        std::cout << "      • ID " << std::setw(2) << gate.id << " : "
                  << std::setw(6) << gateTypeToString(gate.type)
                  << " \"" << (gate.label.empty() ? "-" : gate.label) << "\""
                  << "  [Value=" << gate.outputValue << "]\n";
    }
}


// =============================================================
// ASCII CIRCUIT SCHEMATIC DIAGRAMS
// =============================================================

void printSchematicHalfAdder() {
    std::cout << "\n+-------------------------------------------------------------+\n";
    std::cout << "|               HALF ADDER SCHEMATIC DIAGRAM                  |\n";
    std::cout << "+-------------------------------------------------------------+\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  INPUT A (G0) ---+--------------------> [ XOR: G2 ] ------> OUTPUT Sum (G4)\n";
    std::cout << "|                  |                          ^               |\n";
    std::cout << "|                  |       +------------------+               |\n";
    std::cout << "|                  |       |                                  |\n";
    std::cout << "|  INPUT B (G1) ---+-------+------------> [ AND: G3 ] ------> OUTPUT Carry (G5)\n";
    std::cout << "|                          |                  ^               |\n";
    std::cout << "|                          +------------------+               |\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  Boolean Logic Equations:                                   |\n";
    std::cout << "|    • Sum   = A XOR B                                        |\n";
    std::cout << "|    • Carry = A AND B                                        |\n";
    std::cout << "+-------------------------------------------------------------+\n";
}

void printSchematicNOR() {
    std::cout << "\n+-------------------------------------------------------------+\n";
    std::cout << "|                 NOR GATE SCHEMATIC DIAGRAM                  |\n";
    std::cout << "+-------------------------------------------------------------+\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  INPUT A (G0) ---+                                          |\n";
    std::cout << "|                  +---> [ OR: G2 ] ---> [ NOT: G3 ] -------> OUTPUT Y (G4)\n";
    std::cout << "|  INPUT B (G1) ---+                                          |\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  Boolean Logic Equation:                                    |\n";
    std::cout << "|    • Y = NOT(A OR B)                                        |\n";
    std::cout << "|    • Outputs HIGH (1) if and only if BOTH inputs are 0      |\n";
    std::cout << "+-------------------------------------------------------------+\n";
}

void printSchematicMux2to1() {
    std::cout << "\n+-------------------------------------------------------------+\n";
    std::cout << "|             2-TO-1 MULTIPLEXER SCHEMATIC DIAGRAM            |\n";
    std::cout << "+-------------------------------------------------------------+\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  INPUT A (G0) --------------------------> [ AND1: G4 ] ---+ |\n";
    std::cout << "|                                              ^            | |\n";
    std::cout << "|  INPUT Sel(G2) ---> [ NOT_S: G3 ] -----------+            +-+--> [ OR1: G6 ] ---> OUTPUT Y (G7)\n";
    std::cout << "|       |                                                   | |\n";
    std::cout << "|       +---------------------------------> [ AND2: G5 ] ---+ |\n";
    std::cout << "|                                              ^              |\n";
    std::cout << "|  INPUT B (G1) -------------------------------+              |\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  Boolean Logic Equation:                                    |\n";
    std::cout << "|    • Y = (A AND NOT Sel) OR (B AND Sel)                     |\n";
    std::cout << "|    • When Sel = 0  ===>  Output Y routes Input A            |\n";
    std::cout << "|    • When Sel = 1  ===>  Output Y routes Input B            |\n";
    std::cout << "+-------------------------------------------------------------+\n";
}

void printSchematicISCAS_c17() {
    std::cout << "\n+-------------------------------------------------------------+\n";
    std::cout << "|         IEEE ISCAS '85 BENCHMARK c17 SCHEMATIC              |\n";
    std::cout << "+-------------------------------------------------------------+\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  N1 (G0) --------> [ G10: NAND ] -------------------------+ |\n";
    std::cout << "|                       ^                                   | |\n";
    std::cout << "|  N3 (G2) ---+---------+                                   +-+--> [ G22: NAND ] ---> OUTPUT N22(G11)\n";
    std::cout << "|             |                                             | |\n";
    std::cout << "|             +----> [ G11: NAND ] ----> [ G16: NAND ] -----+ |\n";
    std::cout << "|                       ^                   ^                 |\n";
    std::cout << "|  N6 (G3) -------------+                   |                 |\n";
    std::cout << "|                                           |                 |\n";
    std::cout << "|  N2 (G1) ---------------------------------+                 |\n";
    std::cout << "|                                           |                 |\n";
    std::cout << "|  N7 (G4) ----------------+                +---------------+ |\n";
    std::cout << "|                          v                                | |\n";
    std::cout << "|                    [ G19: NAND ] <------------------------+ |\n";
    std::cout << "|                          |                                  |\n";
    std::cout << "|                          +----------------------------------+--> [ G23: NAND ] ---> OUTPUT N23(G12)\n";
    std::cout << "|                                                             |\n";
    std::cout << "|  Netlist Specs: 5 Inputs, 6 NAND gates, 2 Outputs           |\n";
    std::cout << "|  Standard International Benchmark from IEEE/ACM ISCAS '85   |\n";
    std::cout << "+-------------------------------------------------------------+\n";
}

void showDynamicSchematic(const Circuit& circuit) {
    if (circuit.gates.empty()) {
        std::cout << "\n  [Circuit is empty. No schematic to display.]\n";
        return;
    }

    std::cout << "\n+-------------------------------------------------------------+\n";
    std::cout << "|                 CIRCUIT SCHEMATIC FLOWCHART                 |\n";
    std::cout << "+-------------------------------------------------------------+\n";

    for (const auto& g : circuit.gates) {
        if (g.type == GateType::INPUT) {
            std::cout << "  [INPUT: " << g.label << " (G" << g.id << ")] ";
            if (!circuit.adjList[g.id].empty()) {
                std::cout << "---------------------> Feeds: ";
                for (int outId : circuit.adjList[g.id]) {
                    std::cout << "G" << outId << "[" << circuit.gates[outId].label << "] ";
                }
            }
            std::cout << "\n";
        } else if (g.type == GateType::OUTPUT) {
            std::cout << "  [OUTPUT: " << g.label << " (G" << g.id << ")] <--------------------- Driven by: ";
            if (!g.inputGateIds.empty()) {
                std::cout << "G" << g.inputGateIds[0] << "[" << circuit.gates[g.inputGateIds[0]].label << "]";
            } else {
                std::cout << "(floating)";
            }
            std::cout << "\n";
        } else {
            std::cout << "      | \n";
            std::cout << "      +---> [" << gateTypeToString(g.type) << ": " << g.label << " (G" << g.id << ")]\n";
            std::cout << "            Inputs: ";
            for (int inId : g.inputGateIds) {
                std::cout << "G" << inId << "[" << circuit.gates[inId].label << "] ";
            }
            std::cout << "\n            Drives: ";
            for (int outId : circuit.adjList[g.id]) {
                std::cout << "G" << outId << "[" << circuit.gates[outId].label << "] ";
            }
            std::cout << "\n";
        }
    }
    std::cout << "+-------------------------------------------------------------+\n";
}


// =============================================================
// PRESET DEMO BUILDERS
// =============================================================

void buildHalfAdder(Circuit& circuit) {
    circuit = Circuit();

    int inA = circuit.addGate(GateType::INPUT, "A");       // Gate 0
    int inB = circuit.addGate(GateType::INPUT, "B");       // Gate 1
    int xorG = circuit.addGate(GateType::XOR, "XOR1");     // Gate 2
    int andG = circuit.addGate(GateType::AND, "AND1");     // Gate 3
    int outSum   = circuit.addGate(GateType::OUTPUT, "Sum");    // Gate 4
    int outCarry = circuit.addGate(GateType::OUTPUT, "Carry");  // Gate 5

    circuit.connect(inA, xorG);
    circuit.connect(inB, xorG);
    circuit.connect(inA, andG);
    circuit.connect(inB, andG);
    circuit.connect(xorG, outSum);
    circuit.connect(andG, outCarry);

    std::cout << "\n=============================================================\n";
    std::cout << "             DEMO: HALF ADDER CIRCUIT LOADED                 \n";
    std::cout << "=============================================================\n";
    printSchematicHalfAdder();
    circuit.printCircuit();

    std::cout << "\n[Step 1: Running Initial Simulation with Inputs A=1, B=0]...\n";
    circuit.gates[inA].outputValue = 1;
    circuit.gates[inB].outputValue = 0;
    simulate(circuit, true, false);

    std::cout << "\n[Step 2: Generating Complete Truth Table (All 4 Combinations)]...\n";
    generateTruthTable(circuit);
}

void buildNOR(Circuit& circuit) {
    circuit = Circuit();

    int inA  = circuit.addGate(GateType::INPUT,  "A");      // Gate 0
    int inB  = circuit.addGate(GateType::INPUT,  "B");      // Gate 1
    int orG  = circuit.addGate(GateType::OR,     "OR1");    // Gate 2
    int notG = circuit.addGate(GateType::NOT,    "NOT1");   // Gate 3
    int outY = circuit.addGate(GateType::OUTPUT, "Y");      // Gate 4

    circuit.connect(inA, orG);
    circuit.connect(inB, orG);
    circuit.connect(orG, notG);
    circuit.connect(notG, outY);

    std::cout << "\n=============================================================\n";
    std::cout << "               DEMO: NOR GATE CIRCUIT LOADED                 \n";
    std::cout << "=============================================================\n";
    printSchematicNOR();
    circuit.printCircuit();

    std::cout << "\n[Step 1: Running Initial Simulation with Inputs A=0, B=0]...\n";
    circuit.gates[inA].outputValue = 0;
    circuit.gates[inB].outputValue = 0;
    simulate(circuit, true, false);

    std::cout << "\n[Step 2: Generating Complete Truth Table (All 4 Combinations)]...\n";
    generateTruthTable(circuit);
}

void buildMux2to1(Circuit& circuit) {
    circuit = Circuit();

    int inA = circuit.addGate(GateType::INPUT, "A");        // Gate 0
    int inB = circuit.addGate(GateType::INPUT, "B");        // Gate 1
    int inS = circuit.addGate(GateType::INPUT, "Sel");      // Gate 2

    int notS = circuit.addGate(GateType::NOT,  "NOT_S");    // Gate 3
    int and1 = circuit.addGate(GateType::AND,  "AND1");     // Gate 4
    int and2 = circuit.addGate(GateType::AND,  "AND2");     // Gate 5
    int orG  = circuit.addGate(GateType::OR,   "OR1");      // Gate 6
    int outY = circuit.addGate(GateType::OUTPUT, "Y");      // Gate 7

    circuit.connect(inS, notS);
    circuit.connect(inA, and1);
    circuit.connect(notS, and1);
    circuit.connect(inB, and2);
    circuit.connect(inS, and2);
    circuit.connect(and1, orG);
    circuit.connect(and2, orG);
    circuit.connect(orG, outY);

    std::cout << "\n=============================================================\n";
    std::cout << "          DEMO: 2-TO-1 MULTIPLEXER CIRCUIT LOADED            \n";
    std::cout << "=============================================================\n";
    printSchematicMux2to1();
    circuit.printCircuit();

    std::cout << "\n[Step 1: Running Initial Simulation with A=1, B=0, Sel=0 => Y should be A (1)]...\n";
    circuit.gates[inA].outputValue = 1;
    circuit.gates[inB].outputValue = 0;
    circuit.gates[inS].outputValue = 0;
    simulate(circuit, true, false);

    std::cout << "\n[Step 2: Generating Complete Truth Table (All 8 Combinations)]...\n";
    generateTruthTable(circuit);
}

void buildISCAS85_c17(Circuit& circuit) {
    circuit = Circuit();

    int in1 = circuit.addGate(GateType::INPUT, "N1"); // Gate 0
    int in2 = circuit.addGate(GateType::INPUT, "N2"); // Gate 1
    int in3 = circuit.addGate(GateType::INPUT, "N3"); // Gate 2
    int in6 = circuit.addGate(GateType::INPUT, "N6"); // Gate 3
    int in7 = circuit.addGate(GateType::INPUT, "N7"); // Gate 4

    int g10 = circuit.addGate(GateType::NAND, "G10"); // Gate 5: NAND(N1, N3)
    int g11 = circuit.addGate(GateType::NAND, "G11"); // Gate 6: NAND(N3, N6)
    int g16 = circuit.addGate(GateType::NAND, "G16"); // Gate 7: NAND(N2, G11)
    int g19 = circuit.addGate(GateType::NAND, "G19"); // Gate 8: NAND(G11, N7)
    int g22 = circuit.addGate(GateType::NAND, "G22"); // Gate 9: NAND(G10, G16)
    int g23 = circuit.addGate(GateType::NAND, "G23"); // Gate 10: NAND(G16, G19)

    int out22 = circuit.addGate(GateType::OUTPUT, "N22"); // Gate 11
    int out23 = circuit.addGate(GateType::OUTPUT, "N23"); // Gate 12

    circuit.connect(in1, g10);
    circuit.connect(in3, g10);
    circuit.connect(in3, g11);
    circuit.connect(in6, g11);
    circuit.connect(in2, g16);
    circuit.connect(g11, g16);
    circuit.connect(g11, g19);
    circuit.connect(in7, g19);
    circuit.connect(g10, g22);
    circuit.connect(g16, g22);
    circuit.connect(g16, g23);
    circuit.connect(g19, g23);
    circuit.connect(g22, out22);
    circuit.connect(g23, out23);

    std::cout << "\n=============================================================\n";
    std::cout << "      DEMO: IEEE ISCAS '85 BENCHMARK c17 CIRCUIT LOADED      \n";
    std::cout << "=============================================================\n";
    printSchematicISCAS_c17();
    circuit.printCircuit();

    std::cout << "\n[Step 1: Running Initial Simulation with Inputs All Zero]...\n";
    simulate(circuit, true, false);

    std::cout << "\n[Step 2: Generating Exhaustive Truth Table (All 32 Rows)]...\n";
    generateTruthTable(circuit);
}


// =============================================================
// MAIN INTERACTIVE CLI LOOP
// =============================================================
int main() {
    std::cout << "\n";
    std::cout << "**************************************************************\n";
    std::cout << "*              DIGITAL LOGIC CIRCUIT SIMULATOR               *\n";
    std::cout << "*        Advanced Data Structures & Algorithms Project       *\n";
    std::cout << "*                                                            *\n";
    std::cout << "*  Team Members:                                             *\n";
    std::cout << "*    • Markanda Meher  (Roll No. 206126020)                  *\n";
    std::cout << "*    • Nikhil          (Roll No. 206126021)                  *\n";
    std::cout << "**************************************************************\n";

    Circuit circuit;
    bool running = true;

    // Load default starter circuit (Half Adder)
    std::cout << "\n  [Tip] Loading default Half Adder circuit to start. Feel free to modify or build custom circuits!\n";
    buildHalfAdder(circuit);

    while (running) {
        printMenu();

        int choice;
        if (!readInt(choice)) {
            std::cout << "  [!] Invalid input. Please enter a valid number (0-14).\n";
            continue;
        }

        switch (choice) {

            // ================= 1. ADD GATE =================
            case 1: {
                std::cout << "\n+-------------------------------------------------------------+\n";
                std::cout << "|                      ADD A NEW GATE                         |\n";
                std::cout << "+-------------------------------------------------------------+\n";
                GateType type = selectGateType();

                std::cout << "    Enter human-readable label (e.g., A, B, AND1, Carry): ";
                std::string label;
                std::cin >> label;

                int id = circuit.addGate(type, label);
                std::cout << "\n  [+] Successfully added Gate ID " << id
                          << " [" << gateTypeToString(type) << " \"" << label << "\"]\n";
                break;
            }

            // ================= 2. CONNECT GATES =================
            case 2: {
                std::cout << "\n+-------------------------------------------------------------+\n";
                std::cout << "|                 CONNECT GATES (DRAW WIRE)                   |\n";
                std::cout << "+-------------------------------------------------------------+\n";
                if (circuit.gates.size() < 2) {
                    std::cout << "  [!] Need at least 2 gates in circuit to connect. Add more gates first.\n";
                    break;
                }

                listGatesCompact(circuit);

                std::cout << "\n    Enter SOURCE Gate ID (Output sender): ";
                int fromId;
                if (!readInt(fromId)) break;

                std::cout << "    Enter TARGET Gate ID (Input receiver): ";
                int toId;
                if (!readInt(toId)) break;

                try {
                    circuit.connect(fromId, toId);
                    std::cout << "\n  [+] Wire connected successfully!\n"
                              << "      Gate " << fromId << " [" << circuit.gates[fromId].label << "]"
                              << " ===(wire)===> Gate " << toId << " [" << circuit.gates[toId].label << "]\n";
                } catch (const std::exception& e) {
                    std::cout << "  [!] Error connecting wire: " << e.what() << "\n";
                }
                break;
            }

            // ================= 3. SET INPUT VALUE =================
            case 3: {
                std::cout << "\n+-------------------------------------------------------------+\n";
                std::cout << "|                   SET PRIMARY INPUT VALUE                   |\n";
                std::cout << "+-------------------------------------------------------------+\n";

                bool hasInputs = false;
                std::cout << "  Current Primary Input Pins:\n";
                for (const auto& gate : circuit.gates) {
                    if (gate.type == GateType::INPUT) {
                        std::cout << "    • ID " << gate.id << " [\"" << gate.label << "\"] = "
                                  << gate.outputValue << " (" << (gate.outputValue == 1 ? "HIGH" : "LOW") << ")\n";
                        hasInputs = true;
                    }
                }

                if (!hasInputs) {
                    std::cout << "  [!] No INPUT gates found in circuit. Add an INPUT gate first.\n";
                    break;
                }

                std::cout << "\n    Enter Gate ID to change: ";
                int gateId;
                if (!readInt(gateId)) break;

                if (gateId < 0 || gateId >= static_cast<int>(circuit.gates.size())) {
                    std::cout << "  [!] Gate ID out of range.\n";
                    break;
                }

                if (circuit.gates[gateId].type != GateType::INPUT) {
                    std::cout << "  [!] Gate ID " << gateId << " is a " << gateTypeToString(circuit.gates[gateId].type)
                              << " gate, not a Primary INPUT pin.\n";
                    break;
                }

                std::cout << "    Enter new binary value (0 or 1): ";
                int val;
                if (!readInt(val) || (val != 0 && val != 1)) {
                    std::cout << "  [!] Invalid value. Logic levels must be strictly 0 or 1.\n";
                    break;
                }

                circuit.gates[gateId].outputValue = val;
                std::cout << "\n  [✓] Input Gate " << gateId << " [\"" << circuit.gates[gateId].label
                          << "\"] updated to " << val << " (" << (val == 1 ? "HIGH" : "LOW") << ")\n";
                break;
            }

            // ================= 4. PRINT CIRCUIT TABLE =================
            case 4: {
                circuit.printCircuit();
                break;
            }

            // ================= 5. VIEW SIGNAL FLOW =================
            case 5: {
                circuit.printSignalFlow();
                break;
            }

            // ================= 6. VIEW SCHEMATIC DIAGRAM =================
            case 6: {
                std::cout << "\n  Displaying Circuit Schematic Diagram:\n";
                showDynamicSchematic(circuit);
                break;
            }

            // ================= 7. INSPECT GATE =================
            case 7: {
                std::cout << "\n+-------------------------------------------------------------+\n";
                std::cout << "|                 INSPECT GATE / WIRE PROBE                   |\n";
                std::cout << "+-------------------------------------------------------------+\n";
                listGatesCompact(circuit);
                std::cout << "\n    Enter Gate ID to inspect in detail: ";
                int gId;
                if (readInt(gId)) {
                    circuit.inspectGate(gId);
                }
                break;
            }

            // ================= 8. CHECK FOR CYCLES =================
            case 8: {
                std::cout << "\n+-------------------------------------------------------------+\n";
                std::cout << "|            CYCLE & FEEDBACK LOOP DETECTION (DFS)            |\n";
                std::cout << "+-------------------------------------------------------------+\n";
                if (circuit.gates.empty()) {
                    std::cout << "  [!] Circuit is empty.\n";
                    break;
                }

                if (hasCycle(circuit)) {
                    std::cout << "\n  RESULT: [CYCLE DETECTED]! Circuit topology is INVALID.\n";
                    std::cout << "  Combinational logic circuits cannot contain feedback loops.\n";
                } else {
                    std::cout << "\n  RESULT: [NO CYCLES FOUND]. Circuit is a valid DAG!\n";
                    std::cout << "  Topological sort and levelized evaluation can proceed safely.\n";
                }
                break;
            }

            // ================= 9. SIMULATE =================
            case 9: {
                if (circuit.gates.empty()) {
                    std::cout << "\n  [!] Circuit is empty. Add gates first.\n";
                    break;
                }

                std::cout << "\n  Simulation Execution Options:\n";
                std::cout << "    1. Instant Full Simulation (Complete signal flow trace)\n";
                std::cout << "    2. Interactive Step-by-Step Walkthrough (Gate by gate pause)\n";
                std::cout << "  Choose mode (1 or 2): ";
                int simMode;
                if (!readInt(simMode) || (simMode != 1 && simMode != 2)) {
                    simMode = 1;
                }

                // If step-by-step, consume trailing newline
                if (simMode == 2) {
                    std::string dummy;
                    std::getline(std::cin, dummy);
                }

                simulate(circuit, true, (simMode == 2));
                break;
            }

            // ================= 10. TRUTH TABLE =================
            case 10: {
                if (circuit.gates.empty()) {
                    std::cout << "\n  [!] Circuit is empty.\n";
                    break;
                }
                generateTruthTable(circuit);
                break;
            }

            // ================= 11. DEMO: HALF ADDER =================
            case 11: {
                buildHalfAdder(circuit);
                break;
            }

            // ================= 12. DEMO: NOR GATE =================
            case 12: {
                buildNOR(circuit);
                break;
            }

            // ================= 13. DEMO: 2-to-1 MUX =================
            case 13: {
                buildMux2to1(circuit);
                break;
            }

            // ================= 14. DEMO: ISCAS c17 =================
            case 14: {
                buildISCAS85_c17(circuit);
                break;
            }

            // ================= 0. EXIT =================
            case 0: {
                std::cout << "\n  Thank you for using the Digital Logic Circuit Simulator!\n";
                std::cout << "  Good luck with your project presentation on October 12th!\n\n";
                running = false;
                break;
            }

            default:
                std::cout << "  [!] Unknown option. Please select 0 to 14.\n";
                break;
        }
    }

    return 0;
}
