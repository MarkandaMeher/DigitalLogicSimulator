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
    // printCircuit: Displays the entire circuit structure.
    //               Shows each gate and its outgoing connections.
    //
    //   Useful for debugging and verifying your circuit topology.
    // ---------------------------------------------------------
    void printCircuit() const {
        std::cout << "\n===== Circuit Structure =====\n";
        std::cout << "Total gates: " << gates.size() << "\n\n";

        for (const auto& gate : gates) {
            // Print gate info
            std::cout << "[Gate " << gate.id << "] "
                      << gateTypeToString(gate.type);
            if (!gate.label.empty()) {
                std::cout << " (\"" << gate.label << "\")";
            }
            std::cout << "\n";

            // Print who feeds INTO this gate
            std::cout << "   Inputs from: ";
            if (gate.inputGateIds.empty()) {
                std::cout << "(none)";
            } else {
                for (int inId : gate.inputGateIds) {
                    std::cout << inId << " ";
                }
            }
            std::cout << "\n";

            // Print who this gate feeds INTO (forward edges)
            std::cout << "   Outputs to:  ";
            if (adjList[gate.id].empty()) {
                std::cout << "(none)";
            } else {
                for (int outId : adjList[gate.id]) {
                    std::cout << outId << " ";
                }
            }
            std::cout << "\n\n";
        }
        std::cout << "=============================\n";
    }
};

#endif // CIRCUIT_H
