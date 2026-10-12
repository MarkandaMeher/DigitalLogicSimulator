// =============================================================
// Circuit.h — The DAG structure using an Adjacency List
// =============================================================
// The Circuit class is the GRAPH that holds all gates (nodes)
// and wires (edges). It uses:
//
//   gates    — A vector of all Gate objects (indexed by gate id)
//   adjList  — adjList[i] = list of gate IDs that gate i
//              sends its output TO (forward edges)
//
// This separation is key:
//   - adjList gives us forward edges  (gate i → gate j)
//   - gate.inputGateIds gives us reverse edges (who feeds me?)
//
// We maintain BOTH directions because:
//   - Forward edges (adjList) are used for DFS traversal,
//     cycle detection, and topological sort propagation
//   - Reverse edges (inputGateIds) are used during gate
//     evaluation to fetch input values
// =============================================================

#ifndef CIRCUIT_H
#define CIRCUIT_H

#include "Gate.h"
#include <vector>
#include <iostream>
#include <iomanip>
#include <stdexcept>

class Circuit {
public:
    // All gates in the circuit, indexed by their id
    std::vector<Gate> gates;

    // Adjacency List: adjList[i] contains the IDs of all gates
    // that gate i sends its output to (forward edges / wires)
    std::vector<std::vector<int>> adjList;

    // ---------------------------------------------------------
    // addGate: Creates a new gate and adds it to the circuit.
    //
    //   type  — The kind of gate (AND, OR, NOT, XOR, INPUT, OUTPUT)
    //   label — Optional human-readable name
    //
    //   Returns: The unique id assigned to this gate
    //
    //   Time Complexity: O(1) amortized (vector push_back)
    // ---------------------------------------------------------
    int addGate(GateType type, const std::string& label = "") {
        int id = static_cast<int>(gates.size());  // Next available index
        gates.emplace_back(id, type, label);       // Create the gate
        adjList.emplace_back();                    // Empty adjacency list for it
        return id;
    }

    // ---------------------------------------------------------
    // connect: Draws a wire from one gate's output to another
    //          gate's input. This creates:
    //
    //   1. A forward edge:  adjList[fromId] includes toId
    //   2. A reverse edge:  gates[toId].inputGateIds includes fromId
    //
    //   fromId — The gate sending its output
    //   toId   — The gate receiving the input
    //
    //   Time Complexity: O(1) amortized
    // ---------------------------------------------------------
    void connect(int fromId, int toId) {
        // Bounds checking
        if (fromId < 0 || fromId >= static_cast<int>(gates.size()) ||
            toId   < 0 || toId   >= static_cast<int>(gates.size())) {
            throw std::out_of_range("connect(): Invalid gate ID");
        }

        // Forward edge: fromId → toId
        adjList[fromId].push_back(toId);

        // Reverse edge: toId knows that fromId feeds into it
        gates[toId].inputGateIds.push_back(fromId);
    }

    // ---------------------------------------------------------
    // printSummary: Displays high-level stats of the circuit.
    // ---------------------------------------------------------
    void printSummary() const {
        int inputs = 0, outputs = 0, logic = 0, wires = 0;
        for (const auto& g : gates) {
            if (g.type == GateType::INPUT) inputs++;
            else if (g.type == GateType::OUTPUT) outputs++;
            else logic++;
            wires += static_cast<int>(adjList[g.id].size());
        }

        std::cout << "\n+-------------------------------------------------------------+\n";
        std::cout << "|                     CIRCUIT SUMMARY CARD                    |\n";
        std::cout << "+-------------------------------------------------------------+\n";
        std::cout << "| Total Gates (Nodes):   " << std::setw(4) << gates.size() << "                                 |\n";
        std::cout << "| Primary Inputs:        " << std::setw(4) << inputs << "  (Data entry points)             |\n";
        std::cout << "| Internal Logic Gates:  " << std::setw(4) << logic << "  (Boolean processing units)      |\n";
        std::cout << "| Primary Outputs:       " << std::setw(4) << outputs << "  (Result probes)                 |\n";
        std::cout << "| Total Wires (Edges):   " << std::setw(4) << wires << "  (Directed signal lines)         |\n";
        std::cout << "+-------------------------------------------------------------+\n";
    }

    // ---------------------------------------------------------
    // printCircuit: Displays the entire circuit structure as a
    //               clean, formatted ASCII routing table.
    // ---------------------------------------------------------
    void printCircuit() const {
        if (gates.empty()) {
            std::cout << "\n  [Circuit is currently empty. Add gates to begin!]\n";
            return;
        }

        printSummary();

        std::cout << "\n+-----+----------+---------------+---------------------------+---------------------------+\n";
        std::cout << "| ID  | Type     | Label         | Driven By (Fan-In)        | Drives (Fan-Out)          |\n";
        std::cout << "+-----+----------+---------------+---------------------------+---------------------------+\n";

        for (const auto& gate : gates) {
            std::string typeStr = gateTypeToString(gate.type);
            std::string labelStr = gate.label.empty() ? "-" : ("\"" + gate.label + "\"");

            // Format inputs (Fan-in)
            std::string inStr = "";
            if (gate.type == GateType::INPUT) {
                inStr = "[User Input Pin]";
            } else if (gate.inputGateIds.empty()) {
                inStr = "(floating/unconnected)";
            } else {
                for (size_t i = 0; i < gate.inputGateIds.size(); i++) {
                    int inId = gate.inputGateIds[i];
                    inStr += "G" + std::to_string(inId);
                    if (!gates[inId].label.empty()) inStr += "[" + gates[inId].label + "]";
                    if (i + 1 < gate.inputGateIds.size()) inStr += ", ";
                }
            }

            // Format outputs (Fan-out)
            std::string outStr = "";
            if (gate.type == GateType::OUTPUT) {
                outStr = "[Circuit Output Pin]";
            } else if (adjList[gate.id].empty()) {
                outStr = "(unused/dangling)";
            } else {
                for (size_t i = 0; i < adjList[gate.id].size(); i++) {
                    int outId = adjList[gate.id][i];
                    outStr += "-> G" + std::to_string(outId);
                    if (!gates[outId].label.empty()) outStr += "[" + gates[outId].label + "]";
                    if (i + 1 < adjList[gate.id].size()) outStr += ", ";
                }
            }

            if (inStr.length() > 25) inStr = inStr.substr(0, 22) + "...";
            if (outStr.length() > 25) outStr = outStr.substr(0, 22) + "...";

            std::cout << "| " << std::left << std::setw(4) << gate.id
                      << "| " << std::setw(9) << typeStr
                      << "| " << std::setw(14) << labelStr
                      << "| " << std::setw(26) << inStr
                      << "| " << std::setw(26) << outStr
                      << "|\n";
        }
        std::cout << "+-----+----------+---------------+---------------------------+---------------------------+\n";
    }

    // ---------------------------------------------------------
    // inspectGate: Detailed individual gate diagnostic inspector.
    // ---------------------------------------------------------
    void inspectGate(int gateId) const {
        if (gateId < 0 || gateId >= static_cast<int>(gates.size())) {
            std::cout << "  [!] Invalid Gate ID: " << gateId << "\n";
            return;
        }

        const Gate& g = gates[gateId];
        std::cout << "\n+-------------------------------------------------------------+\n";
        std::cout << "|                    GATE INSPECTION REPORT                   |\n";
        std::cout << "+-------------------------------------------------------------+\n";
        std::cout << "  Gate ID:         " << g.id << "\n";
        std::cout << "  Gate Type:       " << gateTypeToString(g.type) << "\n";
        std::cout << "  Gate Label:      " << (g.label.empty() ? "(none)" : g.label) << "\n";
        std::cout << "  Current Output:  " << g.outputValue << " (" << (g.outputValue == 1 ? "HIGH / 1" : "LOW / 0") << ")\n";
        std::cout << "  -------------------------------------------------------------\n";
        std::cout << "  FAN-IN (Incoming Signal Wires):\n";
        if (g.type == GateType::INPUT) {
            std::cout << "    • Primary Input Pin (Signal controlled by user)\n";
        } else if (g.inputGateIds.empty()) {
            std::cout << "    • [WARNING] Floating Gate! No incoming wire connected.\n";
        } else {
            for (size_t i = 0; i < g.inputGateIds.size(); i++) {
                int inId = g.inputGateIds[i];
                const Gate& src = gates[inId];
                std::cout << "    • Wire #" << (i + 1) << " from Gate " << inId
                          << " [" << gateTypeToString(src.type) << " \"" << src.label << "\"]"
                          << "  => Current Signal = " << src.outputValue << "\n";
            }
        }
        std::cout << "  -------------------------------------------------------------\n";
        std::cout << "  FAN-OUT (Outgoing Signal Wires):\n";
        if (g.type == GateType::OUTPUT) {
            std::cout << "    • Primary Output Pin (Observed circuit result)\n";
        } else if (adjList[g.id].empty()) {
            std::cout << "    • (Dangling output - does not drive any downstream gates)\n";
        } else {
            for (size_t i = 0; i < adjList[g.id].size(); i++) {
                int outId = adjList[g.id][i];
                const Gate& dst = gates[outId];
                std::cout << "    • Drives Gate " << outId
                          << " [" << gateTypeToString(dst.type) << " \"" << dst.label << "\"]\n";
            }
        }
        std::cout << "+-------------------------------------------------------------+\n";
    }

    // ---------------------------------------------------------
    // printSignalFlow: Visualizes the signal propagation flow
    //                  stage-by-stage from Inputs to Outputs.
    // ---------------------------------------------------------
    void printSignalFlow() const {
        if (gates.empty()) {
            std::cout << "  [Circuit is currently empty]\n";
            return;
        }

        std::cout << "\n+-------------------------------------------------------------+\n";
        std::cout << "|                 CIRCUIT SIGNAL FLOW MAP                     |\n";
        std::cout << "+-------------------------------------------------------------+\n";

        std::cout << "\n[STAGE 1: PRIMARY INPUT SIGNALS]\n";
        for (const auto& g : gates) {
            if (g.type == GateType::INPUT) {
                std::cout << "  [" << g.label << " (ID " << g.id << ")] = " << g.outputValue << " ";
                if (!adjList[g.id].empty()) {
                    std::cout << "===> Feeds into: ";
                    for (int outId : adjList[g.id]) {
                        std::cout << "G" << outId << "[" << gates[outId].label << "] ";
                    }
                }
                std::cout << "\n";
            }
        }

        std::cout << "\n[STAGE 2: LOGIC GATES (BOOLEAN PROCESSING)]\n";
        for (const auto& g : gates) {
            if (g.type != GateType::INPUT && g.type != GateType::OUTPUT) {
                std::cout << "  +-- [" << gateTypeToString(g.type) << " \"" << g.label << "\" (ID " << g.id << ")]\n";
                std::cout << "  |   Receives: ";
                for (size_t i = 0; i < g.inputGateIds.size(); i++) {
                    int inId = g.inputGateIds[i];
                    std::cout << "G" << inId << "[" << gates[inId].label << "=" << gates[inId].outputValue << "]";
                    if (i + 1 < g.inputGateIds.size()) std::cout << ", ";
                }
                std::cout << "\n  |   Computes: Output = " << g.outputValue << "\n";
                std::cout << "  |   Propagates to: ";
                if (adjList[g.id].empty()) std::cout << "(none)";
                else {
                    for (int outId : adjList[g.id]) {
                        std::cout << "G" << outId << "[" << gates[outId].label << "] ";
                    }
                }
                std::cout << "\n";
            }
        }

        std::cout << "\n[STAGE 3: PRIMARY OUTPUT RESULTS]\n";
        for (const auto& g : gates) {
            if (g.type == GateType::OUTPUT) {
                std::cout << "  [" << g.label << " (ID " << g.id << ")] = " << g.outputValue;
                if (!g.inputGateIds.empty()) {
                    std::cout << "  <=== Driven by Gate " << g.inputGateIds[0]
                              << " [" << gates[g.inputGateIds[0]].label << "]";
                }
                std::cout << "\n";
            }
        }
        std::cout << "+-------------------------------------------------------------+\n";
    }
};

#endif // CIRCUIT_H
