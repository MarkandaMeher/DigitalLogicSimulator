// =============================================================
// main.cpp — Digital Logic Circuit Simulator (Interactive CLI)
// =============================================================
// Full interactive menu for building, simulating, and testing
// digital combinational logic circuits.
//
// Team: Markanda Meher (206126020) & Nikhil (206126021)
// Course: Advanced Data Structures & Algorithms
// =============================================================

#include "Circuit.h"
#include "Simulator.h"
#include "UnionFind.h"
#include <iostream>
#include <string>
#include <limits>

// ---------------------------------------------------------
// Utility: Clear input buffer after bad input
// ---------------------------------------------------------
void clearInput() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// ---------------------------------------------------------
// Utility: Read an integer safely from the user
// Returns true if a valid integer was read, false otherwise
// ---------------------------------------------------------
bool readInt(int& value) {
    if (std::cin >> value) {
        return true;
    }
    clearInput();
    return false;
}

// ---------------------------------------------------------
// printMenu: Display the main menu options
// ---------------------------------------------------------
void printMenu() {
    std::cout << "\n";
    std::cout << "========================================\n";
    std::cout << "   DIGITAL LOGIC CIRCUIT SIMULATOR\n";
    std::cout << "========================================\n";
    std::cout << "  1. Add Gate\n";
    std::cout << "  2. Connect Gates (Draw Wire)\n";
    std::cout << "  3. Set Input Value\n";
    std::cout << "  4. Print Circuit Structure\n";
    std::cout << "  5. Check for Cycles (DFS)\n";
    std::cout << "  6. Simulate Circuit\n";
    std::cout << "  7. Generate Truth Table\n";
    std::cout << "  8. Demo: Half Adder\n";
    std::cout << "  9. Demo: NOR Gate\n";
    std::cout << " 10. Demo: 2-to-1 Multiplexer\n";
    std::cout << "  0. Exit\n";
    std::cout << "========================================\n";
    std::cout << "  Enter choice: ";
}

// ---------------------------------------------------------
// showGateTypeMenu: Helper for selecting a gate type
// ---------------------------------------------------------
GateType selectGateType() {
    std::cout << "    Gate Types:\n";
    std::cout << "      1. INPUT\n";
    std::cout << "      2. OUTPUT\n";
    std::cout << "      3. AND\n";
    std::cout << "      4. OR\n";
    std::cout << "      5. NOT\n";
    std::cout << "      6. XOR\n";
    std::cout << "    Select type (1-6): ";

    int typeChoice;
    if (!readInt(typeChoice) || typeChoice < 1 || typeChoice > 6) {
        std::cout << "    Invalid type. Defaulting to INPUT.\n";
        return GateType::INPUT;
    }

    switch (typeChoice) {
        case 1: return GateType::INPUT;
        case 2: return GateType::OUTPUT;
        case 3: return GateType::AND;
        case 4: return GateType::OR;
        case 5: return GateType::NOT;
        case 6: return GateType::XOR;
        default: return GateType::INPUT;
    }
}

// ---------------------------------------------------------
// listGates: Show a compact listing of all gates
// ---------------------------------------------------------
void listGates(const Circuit& circuit) {
    if (circuit.gates.empty()) {
        std::cout << "    (no gates in circuit)\n";
        return;
    }
    std::cout << "    Current gates:\n";
    for (const auto& gate : circuit.gates) {
        std::cout << "      [" << gate.id << "] "
                  << gateTypeToString(gate.type);
        if (!gate.label.empty()) {
            std::cout << " \"" << gate.label << "\"";
        }
        std::cout << "\n";
    }
}


// =============================================================
// DEMO CIRCUITS
// =============================================================

// ---------------------------------------------------------
// buildHalfAdder: Constructs a Half Adder circuit
//
//   A Half Adder adds two 1-bit binary numbers:
//     Sum   = A XOR B
//     Carry = A AND B
//
//   Circuit:
//     INPUT_A --+--> [XOR] --> OUTPUT_Sum
//               |
//     INPUT_B --+--> [AND] --> OUTPUT_Carry
// ---------------------------------------------------------
void buildHalfAdder(Circuit& circuit) {
    std::cout << "\n  --- Building Half Adder Demo ---\n";

    // Clear existing circuit by creating a new one
    circuit = Circuit();

    // Add input gates
    int inA = circuit.addGate(GateType::INPUT, "A");       // Gate 0
    int inB = circuit.addGate(GateType::INPUT, "B");       // Gate 1

    // Add logic gates
    int xorG = circuit.addGate(GateType::XOR, "XOR1");     // Gate 2
    int andG = circuit.addGate(GateType::AND, "AND1");     // Gate 3

    // Add output gates
    int outSum   = circuit.addGate(GateType::OUTPUT, "Sum");    // Gate 4
    int outCarry = circuit.addGate(GateType::OUTPUT, "Carry");  // Gate 5

    // Connect wires
    circuit.connect(inA, xorG);     // A -> XOR
    circuit.connect(inB, xorG);     // B -> XOR
    circuit.connect(inA, andG);     // A -> AND
    circuit.connect(inB, andG);     // B -> AND
    circuit.connect(xorG, outSum);  // XOR -> Sum output
    circuit.connect(andG, outCarry);// AND -> Carry output

    std::cout << "  Half Adder built successfully!\n";
    std::cout << "  Gates: A, B (inputs) -> XOR (Sum), AND (Carry) -> Sum, Carry (outputs)\n";

    // Print the circuit
    circuit.printCircuit();

    // Generate truth table
    std::cout << "\n  Generating truth table for Half Adder...\n";
    generateTruthTable(circuit);
}

// ---------------------------------------------------------
// buildNOR: Constructs a NOR gate from OR + NOT
//
//   NOR = NOT(A OR B)
//
//   Circuit:
//     INPUT_A --+
//               |--> [OR] --> [NOT] --> OUTPUT_Y
//     INPUT_B --+
// ---------------------------------------------------------
void buildNOR(Circuit& circuit) {
    std::cout << "\n  --- Building NOR Gate Demo ---\n";

    circuit = Circuit();

    // Add gates
    int inA  = circuit.addGate(GateType::INPUT,  "A");      // Gate 0
    int inB  = circuit.addGate(GateType::INPUT,  "B");      // Gate 1
    int orG  = circuit.addGate(GateType::OR,     "OR1");    // Gate 2
    int notG = circuit.addGate(GateType::NOT,    "NOT1");   // Gate 3
    int outY = circuit.addGate(GateType::OUTPUT, "Y");      // Gate 4

    // Connect wires
    circuit.connect(inA, orG);      // A -> OR
    circuit.connect(inB, orG);      // B -> OR
    circuit.connect(orG, notG);     // OR -> NOT
    circuit.connect(notG, outY);    // NOT -> Y output

    std::cout << "  NOR gate built: Y = NOT(A OR B)\n";

    circuit.printCircuit();

    std::cout << "\n  Generating truth table for NOR...\n";
    generateTruthTable(circuit);
}

// ---------------------------------------------------------
// buildMux2to1: Constructs a 2-to-1 Multiplexer
//
//   A MUX selects one of two inputs based on a select line:
//     Output = (A AND NOT_S) OR (B AND S)
//
//   When S=0, Output=A.  When S=1, Output=B.
//
//   This is a more complex circuit demonstrating how
//   basic gates combine into useful components.
//
//   Circuit:
//     INPUT_A ----> [AND1] --+
//                    ^        |
//     INPUT_S -> [NOT] ------+----> [OR] ----> OUTPUT_Y
//                |                   ^
//                +---> [AND2] ------+
//     INPUT_B -------> ^
// ---------------------------------------------------------
void buildMux2to1(Circuit& circuit) {
    std::cout << "\n  --- Building 2-to-1 Multiplexer Demo ---\n";

    circuit = Circuit();

    // Inputs
    int inA = circuit.addGate(GateType::INPUT, "A");        // Gate 0
    int inB = circuit.addGate(GateType::INPUT, "B");        // Gate 1
    int inS = circuit.addGate(GateType::INPUT, "Sel");      // Gate 2

    // Logic gates
    int notS = circuit.addGate(GateType::NOT,  "NOT_S");    // Gate 3
    int and1 = circuit.addGate(GateType::AND,  "AND1");     // Gate 4: A AND NOT_S
    int and2 = circuit.addGate(GateType::AND,  "AND2");     // Gate 5: B AND S
    int orG  = circuit.addGate(GateType::OR,   "OR1");      // Gate 6

    // Output
    int outY = circuit.addGate(GateType::OUTPUT, "Y");      // Gate 7

    // Wires
    circuit.connect(inS, notS);     // S -> NOT
    circuit.connect(inA, and1);     // A -> AND1
    circuit.connect(notS, and1);    // NOT_S -> AND1  (so AND1 = A AND NOT_S)
    circuit.connect(inB, and2);     // B -> AND2
    circuit.connect(inS, and2);     // S -> AND2      (so AND2 = B AND S)
    circuit.connect(and1, orG);     // AND1 -> OR
    circuit.connect(and2, orG);     // AND2 -> OR     (so OR = (A AND NOT_S) OR (B AND S))
    circuit.connect(orG, outY);     // OR -> output

    std::cout << "  2-to-1 MUX built: Y = (A AND NOT S) OR (B AND S)\n";
    std::cout << "  When Sel=0, Y=A.  When Sel=1, Y=B.\n";

    circuit.printCircuit();

    std::cout << "\n  Generating truth table for 2-to-1 MUX...\n";
    generateTruthTable(circuit);
}


// =============================================================
// MAIN: Interactive CLI Loop
// =============================================================
int main() {
    std::cout << "============================================\n";
    std::cout << "   DIGITAL LOGIC CIRCUIT SIMULATOR\n";
    std::cout << "   Advanced Data Structures & Algorithms\n";
    std::cout << "--------------------------------------------\n";
    std::cout << "   Markanda Meher  (Roll No. 206126020)\n";
    std::cout << "   Nikhil          (Roll No. 206126021)\n";
    std::cout << "============================================\n";

    Circuit circuit;
    bool running = true;

    while (running) {
        printMenu();

        int choice;
        if (!readInt(choice)) {
            std::cout << "  Invalid input. Please enter a number.\n";
            continue;
        }

        switch (choice) {

            // ================= 1. ADD GATE =================
            case 1: {
                std::cout << "\n  --- Add a New Gate ---\n";
                GateType type = selectGateType();

                std::cout << "    Enter label (e.g., A, B, AND1): ";
                std::string label;
                std::cin >> label;

                int id = circuit.addGate(type, label);
                std::cout << "    Gate added: [" << id << "] "
                          << gateTypeToString(type) << " \"" << label << "\"\n";
                break;
            }

            // ================= 2. CONNECT GATES =================
            case 2: {
                std::cout << "\n  --- Connect Gates (Draw Wire) ---\n";
                if (circuit.gates.size() < 2) {
                    std::cout << "    Need at least 2 gates. Add more gates first.\n";
                    break;
                }

                listGates(circuit);

                std::cout << "    From gate ID: ";
                int fromId;
                if (!readInt(fromId)) {
                    std::cout << "    Invalid ID.\n";
                    break;
                }

                std::cout << "    To gate ID:   ";
                int toId;
                if (!readInt(toId)) {
                    std::cout << "    Invalid ID.\n";
                    break;
                }

                try {
                    circuit.connect(fromId, toId);
                    std::cout << "    Wire drawn: Gate " << fromId << " -> Gate " << toId << "\n";
                } catch (const std::out_of_range& e) {
                    std::cout << "    Error: " << e.what() << "\n";
                }
                break;
            }

            // ================= 3. SET INPUT VALUE =================
            case 3: {
                std::cout << "\n  --- Set Input Value ---\n";

                // Show only INPUT gates
                bool hasInputs = false;
                for (const auto& gate : circuit.gates) {
                    if (gate.type == GateType::INPUT) {
                        std::cout << "    [" << gate.id << "] INPUT \""
                                  << gate.label << "\" = " << gate.outputValue << "\n";
                        hasInputs = true;
                    }
                }

                if (!hasInputs) {
                    std::cout << "    No INPUT gates found. Add INPUT gates first.\n";
                    break;
                }

                std::cout << "    Gate ID to set: ";
                int gateId;
                if (!readInt(gateId)) {
                    std::cout << "    Invalid ID.\n";
                    break;
                }

                if (gateId < 0 || gateId >= static_cast<int>(circuit.gates.size())) {
                    std::cout << "    Invalid gate ID.\n";
                    break;
                }

                if (circuit.gates[gateId].type != GateType::INPUT) {
                    std::cout << "    Gate " << gateId << " is not an INPUT gate.\n";
                    break;
                }

                std::cout << "    Value (0 or 1): ";
                int value;
                if (!readInt(value) || (value != 0 && value != 1)) {
                    std::cout << "    Invalid value. Must be 0 or 1.\n";
                    break;
                }

                circuit.gates[gateId].outputValue = value;
                std::cout << "    Input \"" << circuit.gates[gateId].label
                          << "\" set to " << value << "\n";
                break;
            }

            // ================= 4. PRINT CIRCUIT =================
            case 4: {
                if (circuit.gates.empty()) {
                    std::cout << "\n  Circuit is empty. Add some gates first.\n";
                } else {
                    circuit.printCircuit();
                }
                break;
            }

            // ================= 5. CHECK FOR CYCLES =================
            case 5: {
                std::cout << "\n  --- Cycle Detection (DFS) ---\n";
                if (circuit.gates.empty()) {
                    std::cout << "  Circuit is empty.\n";
                    break;
                }

                if (hasCycle(circuit)) {
                    std::cout << "  RESULT: Cycle DETECTED! This circuit is INVALID.\n";
                    std::cout << "  Combinational circuits must not have feedback loops.\n";
                } else {
                    std::cout << "  RESULT: No cycles found. Circuit is a valid DAG.\n";
                }
                break;
            }

            // ================= 6. SIMULATE =================
            case 6: {
                std::cout << "\n  --- Simulate Circuit ---\n";
                if (circuit.gates.empty()) {
                    std::cout << "  Circuit is empty.\n";
                    break;
                }
                simulate(circuit, true);
                break;
            }

            // ================= 7. TRUTH TABLE =================
            case 7: {
                std::cout << "\n  --- Generate Truth Table ---\n";
                if (circuit.gates.empty()) {
                    std::cout << "  Circuit is empty.\n";
                    break;
                }
                generateTruthTable(circuit);
                break;
            }

            // ================= 8. DEMO: HALF ADDER =================
            case 8: {
                buildHalfAdder(circuit);
                break;
            }

            // ================= 9. DEMO: NOR =================
            case 9: {
                buildNOR(circuit);
                break;
            }

            // ================= 10. DEMO: 2-to-1 MUX =================
            case 10: {
                buildMux2to1(circuit);
                break;
            }

            // ================= 0. EXIT =================
            case 0: {
                std::cout << "\n  Goodbye! Thank you for using the simulator.\n\n";
                running = false;
                break;
            }

            default:
                std::cout << "  Invalid choice. Please try again.\n";
                break;
        }
    }

    return 0;
}
