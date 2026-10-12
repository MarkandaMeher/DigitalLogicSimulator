// =============================================================
// Simulator.h — Algorithms for circuit validation & simulation
// =============================================================
// This file contains all the core algorithms:
//
//   1. Cycle Detection  — DFS with 3-colour marking
//   2. Topological Sort — Kahn's BFS-based algorithm
//   3. Gate Evaluation  — Boolean logic per gate type
//   4. Simulation       — Evaluate all gates in topo order
//   5. Truth Table      — Exhaustive enumeration of all inputs
// =============================================================

#ifndef SIMULATOR_H
#define SIMULATOR_H

#include "Circuit.h"
#include <vector>
#include <queue>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <string>

// =============================================================
// SECTION 1: Cycle Detection using Depth-First Search (DFS)
// =============================================================
//
// Combinational circuits MUST be acyclic (no feedback loops).
// We use a 3-colour DFS to detect back edges:
//
//   WHITE (0) — Not yet visited
//   GRAY  (1) — Currently on the DFS recursion stack
//   BLACK (2) — Fully explored, all descendants processed
//
// A cycle exists if and only if DFS encounters a GRAY node
// (a node that is an ancestor in the current DFS path).
// =============================================================

// ---------------------------------------------------------
// hasCycleDFS: Recursive DFS helper for cycle detection.
//
//   node    — Current node being explored
//   color   — Array tracking the state of each node
//   circuit — The circuit graph
//
//   Returns: true if a cycle is detected
//
//   Time Complexity: O(V + E) across all calls
// ---------------------------------------------------------
bool hasCycleDFS(int node, std::vector<int>& color, const Circuit& circuit) {
    // Mark this node as GRAY (currently exploring)
    color[node] = 1;

    // Explore all neighbours (forward edges)
    for (int neighbor : circuit.adjList[node]) {
        if (color[neighbor] == 1) {
            // Found a back edge to an ancestor → CYCLE!
            std::cout << "  [!] Cycle detected: Gate " << node
                      << " (" << gateTypeToString(circuit.gates[node].type) << ")"
                      << " -> Gate " << neighbor
                      << " (" << gateTypeToString(circuit.gates[neighbor].type) << ")"
                      << " forms a back edge!\n";
            return true;
        }
        if (color[neighbor] == 0) {
            // WHITE node — explore it
            if (hasCycleDFS(neighbor, color, circuit)) {
                return true;
            }
        }
        // BLACK nodes (color == 2) are already fully processed — skip
    }

    // All descendants explored, mark as BLACK (done)
    color[node] = 2;
    return false;
}

// ---------------------------------------------------------
// hasCycle: Checks the entire circuit for cycles.
//
//   Runs DFS from every unvisited node to handle
//   disconnected components.
//
//   Returns: true if any cycle is found
//
//   Time Complexity: O(V + E)
//   Space Complexity: O(V) for the color array
// ---------------------------------------------------------
bool hasCycle(const Circuit& circuit) {
    int n = static_cast<int>(circuit.gates.size());
    if (n == 0) return false;

    // Initialize all nodes as WHITE (unvisited)
    std::vector<int> color(n, 0);

    // Run DFS from every unvisited node
    for (int i = 0; i < n; i++) {
        if (color[i] == 0) {
            if (hasCycleDFS(i, color, circuit)) {
                return true;
            }
        }
    }
    return false;
}


// =============================================================
// SECTION 2: Topological Sort — Kahn's Algorithm (BFS-based)
// =============================================================
//
// Determines the order in which gates must be evaluated so
// that every gate is processed ONLY after all its inputs are
// ready.
//
// Algorithm:
//   1. Compute in-degree for every node
//   2. Enqueue all nodes with in-degree 0 (INPUT gates)
//   3. Process queue: dequeue a node, add to sorted order,
//      decrement in-degree of all its neighbours
//   4. If sorted order has all V nodes → valid DAG
//
// Time Complexity:  O(V + E)
// Space Complexity: O(V + E)
// =============================================================

std::vector<int> topologicalSort(const Circuit& circuit) {
    int n = static_cast<int>(circuit.gates.size());

    // Step 1: Compute in-degree for each gate
    // In-degree = number of incoming edges = number of gates
    // that feed into this gate
    std::vector<int> inDegree(n, 0);
    for (int i = 0; i < n; i++) {
        for (int neighbor : circuit.adjList[i]) {
            inDegree[neighbor]++;
        }
    }

    // Step 2: Enqueue all gates with in-degree 0
    // These are typically INPUT gates (no dependencies)
    std::queue<int> q;
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }

    // Step 3: BFS — process gates in dependency order
    std::vector<int> order;
    order.reserve(n);

    while (!q.empty()) {
        int curr = q.front();
        q.pop();
        order.push_back(curr);

        // For each gate that curr feeds into...
        for (int neighbor : circuit.adjList[curr]) {
            // Reduce its in-degree (one dependency satisfied)
            inDegree[neighbor]--;
            // If all dependencies are now satisfied, enqueue it
            if (inDegree[neighbor] == 0) {
                q.push(neighbor);
            }
        }
    }

    // Step 4: Verify — if order doesn't contain all nodes,
    // the graph has a cycle (shouldn't happen if hasCycle()
    // was called first, but this is a safety check)
    if (static_cast<int>(order.size()) != n) {
        std::cout << "  [!] Warning: Topological sort incomplete. "
                  << "Processed " << order.size() << " of " << n
                  << " gates. The circuit may contain a cycle.\n";
    }

    return order;
}


// =============================================================
// SECTION 3: Gate Evaluation — Boolean Logic
// =============================================================
//
// Each gate type implements a specific boolean function:
//
//   AND  — result = 1;  for each input: result &= input
//   OR   — result = 0;  for each input: result |= input
//   NOT  — result = !input (single input only)
//   XOR  — result = 0;  for each input: result ^= input
//   OUTPUT — passes through its single input
//   INPUT  — keeps user-set value (no computation)
// =============================================================

void evaluateGate(Gate& gate, const std::vector<Gate>& allGates) {
    switch (gate.type) {

        case GateType::AND: {
            // AND: Start with 1, bitwise-AND with each input
            // Result is 1 only if ALL inputs are 1
            int result = 1;
            for (int inId : gate.inputGateIds) {
                result &= allGates[inId].outputValue;
            }
            gate.outputValue = result;
            break;
        }

        case GateType::OR: {
            // OR: Start with 0, bitwise-OR with each input
            // Result is 1 if ANY input is 1
            int result = 0;
            for (int inId : gate.inputGateIds) {
                result |= allGates[inId].outputValue;
            }
            gate.outputValue = result;
            break;
        }

        case GateType::NOT: {
            // NOT: Invert the single input (1→0, 0→1)
            if (!gate.inputGateIds.empty()) {
                gate.outputValue = allGates[gate.inputGateIds[0]].outputValue ? 0 : 1;
            }
            break;
        }

        case GateType::XOR: {
            // XOR: Start with 0, XOR with each input
            // Result is 1 if an ODD number of inputs are 1
            int result = 0;
            for (int inId : gate.inputGateIds) {
                result ^= allGates[inId].outputValue;
            }
            gate.outputValue = result;
            break;
        }

        case GateType::NAND: {
            // NAND: Inverted AND
            int result = 1;
            for (int inId : gate.inputGateIds) {
                result &= allGates[inId].outputValue;
            }
            gate.outputValue = (result == 1) ? 0 : 1;
            break;
        }

        case GateType::NOR: {
            // NOR: Inverted OR
            int result = 0;
            for (int inId : gate.inputGateIds) {
                result |= allGates[inId].outputValue;
            }
            gate.outputValue = (result == 1) ? 0 : 1;
            break;
        }

        case GateType::XNOR: {
            // XNOR: Inverted XOR
            int result = 0;
            for (int inId : gate.inputGateIds) {
                result ^= allGates[inId].outputValue;
            }
            gate.outputValue = (result == 1) ? 0 : 1;
            break;
        }

        case GateType::OUTPUT: {
            // OUTPUT: Simply passes through its single input
            if (!gate.inputGateIds.empty()) {
                gate.outputValue = allGates[gate.inputGateIds[0]].outputValue;
            }
            break;
        }

        case GateType::INPUT:
            // INPUT gates keep their user-set value
            // No computation needed
            break;
    }
}


// =============================================================
// SECTION 4: Full Circuit Simulation
// =============================================================
//
// Workflow:
//   1. Check for cycles (halt if found)
//   2. Compute topological order
//   3. Evaluate each gate in that order
//   4. Display results
//
// Time Complexity: O(V + E)
// =============================================================

// ---------------------------------------------------------
// Helper: Generates a human-readable formula string
// for a gate's computation (e.g. "1 AND 0 = 0")
// ---------------------------------------------------------
inline std::string getGateFormulaString(const Gate& gate, const std::vector<Gate>& allGates) {
    if (gate.type == GateType::INPUT) {
        return "User Input = " + std::to_string(gate.outputValue);
    }
    if (gate.type == GateType::OUTPUT) {
        if (gate.inputGateIds.empty()) return "Disconnected (0)";
        int inId = gate.inputGateIds[0];
        return "Pass-through from G" + std::to_string(inId) + " [" + allGates[inId].label + "] = " + std::to_string(gate.outputValue);
    }
    if (gate.type == GateType::NOT) {
        if (gate.inputGateIds.empty()) return "NOT(?)";
        int inVal = allGates[gate.inputGateIds[0]].outputValue;
        return "NOT(" + std::to_string(inVal) + ") = " + std::to_string(gate.outputValue);
    }

    std::string op = gateTypeToString(gate.type);
    std::string expr = "";
    for (size_t i = 0; i < gate.inputGateIds.size(); i++) {
        expr += std::to_string(allGates[gate.inputGateIds[i]].outputValue);
        if (i + 1 < gate.inputGateIds.size()) expr += " " + op + " ";
    }
    return expr + " = " + std::to_string(gate.outputValue);
}

// =============================================================
// SECTION 4: Full Circuit Simulation
// =============================================================
bool simulate(Circuit& circuit, bool verbose = true, bool stepByStep = false) {
    int n = static_cast<int>(circuit.gates.size());
    if (n == 0) {
        if (verbose) std::cout << "\n  [!] Circuit is empty. Nothing to simulate.\n";
        return false;
    }

    // Step 1: Cycle check
    if (hasCycle(circuit)) {
        if (verbose) {
            std::cout << "\n+-------------------------------------------------------------+\n";
            std::cout << "|                 *** SIMULATION HALTED ***                   |\n";
            std::cout << "+-------------------------------------------------------------+\n";
            std::cout << "  ERROR: The circuit contains a circular feedback loop (cycle)!\n";
            std::cout << "  Combinational logic circuits must be acyclic (DAGs).\n";
            std::cout << "  Please remove the feedback wire to simulate.\n";
            std::cout << "+-------------------------------------------------------------+\n";
        }
        return false;
    }

    // Step 2: Topological sort
    std::vector<int> order = topologicalSort(circuit);

    if (verbose) {
        std::cout << "\n+-------------------------------------------------------------+\n";
        std::cout << "|                 CIRCUIT SIMULATION EXECUTION                |\n";
        std::cout << "+-------------------------------------------------------------+\n";
        std::cout << "  TOPOLOGICAL EVALUATION ORDER (Kahn's BFS):\n  ";
        for (size_t i = 0; i < order.size(); i++) {
            int gid = order[i];
            std::cout << "G" << gid << "[" << circuit.gates[gid].label << "]";
            if (i + 1 < order.size()) std::cout << " -> ";
        }
        std::cout << "\n+-------------------------------------------------------------+\n";
    }

    // Step 3: Evaluate each gate in topological order with friendly trace
    int stepNum = 1;
    for (int gateId : order) {
        evaluateGate(circuit.gates[gateId], circuit.gates);
        const auto& g = circuit.gates[gateId];

        if (verbose) {
            std::cout << "  [Step " << stepNum++ << "/" << order.size() << "] ";
            if (g.type == GateType::INPUT) {
                std::cout << "INPUT Gate " << g.id << " (\"" << g.label << "\") = "
                          << g.outputValue << " (" << (g.outputValue == 1 ? "HIGH / 1" : "LOW / 0") << ")\n";
                if (!circuit.adjList[g.id].empty()) {
                    std::cout << "           Signals forward to: ";
                    for (int outId : circuit.adjList[g.id]) {
                        std::cout << "G" << outId << "[" << circuit.gates[outId].label << "] ";
                    }
                    std::cout << "\n";
                }
            } else if (g.type == GateType::OUTPUT) {
                std::cout << "OUTPUT Gate " << g.id << " (\"" << g.label << "\") = "
                          << g.outputValue << " (" << (g.outputValue == 1 ? "HIGH / 1" : "LOW / 0") << ")\n";
                if (!g.inputGateIds.empty()) {
                    std::cout << "           Driven by: Gate " << g.inputGateIds[0]
                              << " [" << circuit.gates[g.inputGateIds[0]].label << "]\n";
                }
            } else {
                std::cout << "Gate " << g.id << " [" << gateTypeToString(g.type) << " \"" << g.label << "\"]\n";
                std::cout << "           Inputs:      ";
                for (size_t i = 0; i < g.inputGateIds.size(); i++) {
                    int inId = g.inputGateIds[i];
                    std::cout << "G" << inId << "[" << circuit.gates[inId].label << "]=" << circuit.gates[inId].outputValue;
                    if (i + 1 < g.inputGateIds.size()) std::cout << ", ";
                }
                std::cout << "\n";
                std::cout << "           Calculation: " << getGateFormulaString(g, circuit.gates) << "\n";
                std::cout << "           Output:      " << g.outputValue << " (" << (g.outputValue == 1 ? "HIGH / 1" : "LOW / 0") << ")\n";
                if (!circuit.adjList[g.id].empty()) {
                    std::cout << "           Signals forward to: ";
                    for (int outId : circuit.adjList[g.id]) {
                        std::cout << "G" << outId << "[" << circuit.gates[outId].label << "] ";
                    }
                    std::cout << "\n";
                }
            }
            std::cout << "  -------------------------------------------------------------\n";

            if (stepByStep && stepNum <= static_cast<int>(order.size())) {
                std::cout << "  >> Press ENTER to advance to next gate...";
                std::string dummy;
                std::getline(std::cin, dummy);
            }
        }
    }

    // Step 4: Display final results dashboard
    if (verbose) {
        std::cout << "\n+-------------------------------------------------------------+\n";
        std::cout << "|                   FINAL SIMULATION DASHBOARD                |\n";
        std::cout << "+-------------------------------------------------------------+\n";
        std::cout << "  PRIMARY INPUTS (APPLIED BY USER):\n";
        for (const auto& gate : circuit.gates) {
            if (gate.type == GateType::INPUT) {
                std::cout << "    • " << std::left << std::setw(10) << gate.label << " (Gate " << gate.id << ") = "
                          << gate.outputValue << " [" << (gate.outputValue == 1 ? "HIGH / 1" : "LOW / 0") << "]\n";
            }
        }

        std::cout << "\n  INTERNAL LOGIC COMPUTATIONS:\n";
        for (const auto& gate : circuit.gates) {
            if (gate.type != GateType::INPUT && gate.type != GateType::OUTPUT) {
                std::cout << "    • " << std::left << std::setw(10) << gate.label << " (Gate " << gate.id << ", "
                          << std::setw(4) << gateTypeToString(gate.type) << ") = " << gate.outputValue
                          << "  [" << getGateFormulaString(gate, circuit.gates) << "]\n";
            }
        }

        std::cout << "\n  PRIMARY OUTPUTS (RESULTING SIGNALS):\n";
        for (const auto& gate : circuit.gates) {
            if (gate.type == GateType::OUTPUT) {
                std::cout << "    • " << std::left << std::setw(10) << gate.label << " (Gate " << gate.id << ") = "
                          << gate.outputValue << " [" << (gate.outputValue == 1 ? "HIGH / 1" : "LOW / 0") << "]\n";
            }
        }
        std::cout << "+-------------------------------------------------------------+\n";
    }

    return true;
}

// =============================================================
// SECTION 5: Truth Table Generation
// =============================================================
void generateTruthTable(Circuit& circuit) {
    int n = static_cast<int>(circuit.gates.size());
    if (n == 0) {
        std::cout << "  [!] Circuit is empty. Nothing to generate.\n";
        return;
    }

    // Step 1: Collect all INPUT and OUTPUT gate IDs
    std::vector<int> inputIds;
    std::vector<int> outputIds;
    for (const auto& gate : circuit.gates) {
        if (gate.type == GateType::INPUT)  inputIds.push_back(gate.id);
        if (gate.type == GateType::OUTPUT) outputIds.push_back(gate.id);
    }

    int numInputs = static_cast<int>(inputIds.size());
    int numOutputs = static_cast<int>(outputIds.size());

    if (numInputs == 0) {
        std::cout << "  [!] No INPUT gates found. Cannot generate truth table.\n";
        return;
    }
    if (numOutputs == 0) {
        std::cout << "  [!] No OUTPUT gates found. Cannot generate truth table.\n";
        return;
    }

    if (numInputs > 20) {
        std::cout << "  [!] Too many inputs (" << numInputs
                  << "). Truth table would require " << (1 << numInputs)
                  << " rows. (Max: 20 inputs)\n";
        return;
    }

    int totalCombinations = 1 << numInputs;  // 2^n
    std::vector<int> highCount(numOutputs, 0);

    std::cout << "\n+-------------------------------------------------------------+\n";
    std::cout << "|                 EXHAUSTIVE TRUTH TABLE (2^" << numInputs << " = " << totalCombinations << ")                |\n";
    std::cout << "+-------------------------------------------------------------+\n  ";

    // Header row
    for (int i = 0; i < numInputs; i++) {
        std::cout << std::setw(6) << circuit.gates[inputIds[i]].label;
    }
    std::cout << "   | ";
    for (int i = 0; i < numOutputs; i++) {
        std::cout << std::setw(8) << circuit.gates[outputIds[i]].label;
    }
    std::cout << "\n  ";

    for (int i = 0; i < numInputs; i++) std::cout << "------";
    std::cout << "---+--";
    for (int i = 0; i < numOutputs; i++) std::cout << "--------";
    std::cout << "\n";

    // Row evaluation
    for (int combo = 0; combo < totalCombinations; combo++) {
        for (int i = 0; i < numInputs; i++) {
            int bitPosition = numInputs - 1 - i;
            circuit.gates[inputIds[i]].outputValue = (combo >> bitPosition) & 1;
        }

        bool success = simulate(circuit, false);
        if (!success) {
            std::cout << "  [!] Simulation failed on combination " << combo << ". Aborting.\n";
            return;
        }

        std::cout << "  ";
        for (int i = 0; i < numInputs; i++) {
            std::cout << std::setw(6) << circuit.gates[inputIds[i]].outputValue;
        }
        std::cout << "   | ";
        for (int i = 0; i < numOutputs; i++) {
            int outVal = circuit.gates[outputIds[i]].outputValue;
            if (outVal == 1) highCount[i]++;
            std::cout << std::setw(8) << outVal;
        }
        std::cout << "\n";
    }

    std::cout << "  ";
    for (int i = 0; i < numInputs; i++) std::cout << "------";
    std::cout << "---+--";
    for (int i = 0; i < numOutputs; i++) std::cout << "--------";
    std::cout << "\n";

    std::cout << "  Total Rows: " << totalCombinations << " (All 2^" << numInputs << " combinations tested)\n";
    std::cout << "  Output Signal Distribution:\n";
    for (int i = 0; i < numOutputs; i++) {
        std::cout << "    • Output [" << circuit.gates[outputIds[i]].label << "]: "
                  << highCount[i] << " HIGHs (1), "
                  << (totalCombinations - highCount[i]) << " LOWs (0)\n";
    }
    std::cout << "+-------------------------------------------------------------+\n";
}

#endif // SIMULATOR_H
