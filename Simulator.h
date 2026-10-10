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

bool simulate(Circuit& circuit, bool verbose = true) {
    int n = static_cast<int>(circuit.gates.size());
    if (n == 0) {
        if (verbose) std::cout << "  Circuit is empty. Nothing to simulate.\n";
        return false;
    }

    // Step 1: Cycle check
    if (hasCycle(circuit)) {
        if (verbose) {
            std::cout << "\n  *** SIMULATION ABORTED ***\n";
            std::cout << "  The circuit contains a feedback loop (cycle).\n";
            std::cout << "  Combinational circuits must be acyclic (DAGs).\n";
        }
        return false;
    }

    // Step 2: Topological sort
    std::vector<int> order = topologicalSort(circuit);

    // Step 3: Evaluate each gate in topological order
    for (int gateId : order) {
        evaluateGate(circuit.gates[gateId], circuit.gates);
    }

    // Step 4: Display results
    if (verbose) {
        std::cout << "\n  --- Simulation Results ---\n";

        // Show input values
        std::cout << "  Inputs:\n";
        for (const auto& gate : circuit.gates) {
            if (gate.type == GateType::INPUT) {
                std::cout << "    " << gate.label << " (Gate " << gate.id
                          << ") = " << gate.outputValue << "\n";
            }
        }

        // Show intermediate gate values
        std::cout << "  Intermediate Gates:\n";
        for (const auto& gate : circuit.gates) {
            if (gate.type != GateType::INPUT && gate.type != GateType::OUTPUT) {
                std::cout << "    " << gateTypeToString(gate.type)
                          << " \"" << gate.label << "\" (Gate " << gate.id
                          << ") = " << gate.outputValue << "\n";
            }
        }

        // Show output values
        std::cout << "  Outputs:\n";
        for (const auto& gate : circuit.gates) {
            if (gate.type == GateType::OUTPUT) {
                std::cout << "    " << gate.label << " (Gate " << gate.id
                          << ") = " << gate.outputValue << "\n";
            }
        }
        std::cout << "  -------------------------\n";
    }

    return true;
}


// =============================================================
// SECTION 5: Truth Table Generation
// =============================================================
//
// Generates the complete truth table for a circuit by:
//   1. Identifying all INPUT gates
//   2. Iterating through all 2^n input combinations
//      (using bit manipulation)
//   3. For each combination: set inputs, simulate, record outputs
//   4. Display a formatted truth table
//
// Time Complexity: O(2^n * (V + E))
//   where n = number of INPUT gates
// =============================================================

void generateTruthTable(Circuit& circuit) {
    int n = static_cast<int>(circuit.gates.size());
    if (n == 0) {
        std::cout << "  Circuit is empty. Nothing to generate.\n";
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
        std::cout << "  No INPUT gates found. Cannot generate truth table.\n";
        return;
    }
    if (numOutputs == 0) {
        std::cout << "  No OUTPUT gates found. Cannot generate truth table.\n";
        return;
    }

    // Safety: Don't attempt if too many inputs (2^20 = 1M rows)
    if (numInputs > 20) {
        std::cout << "  Too many inputs (" << numInputs
                  << "). Truth table would have " << (1 << numInputs)
                  << " rows. Maximum supported: 20 inputs.\n";
        return;
    }

    int totalCombinations = 1 << numInputs;  // 2^n

    // Step 2: Print header
    std::cout << "\n  ===== TRUTH TABLE =====\n  ";
    for (int i = 0; i < numInputs; i++) {
        std::cout << std::setw(6) << circuit.gates[inputIds[i]].label;
    }
    std::cout << "  |";
    for (int i = 0; i < numOutputs; i++) {
        std::cout << std::setw(8) << circuit.gates[outputIds[i]].label;
    }
    std::cout << "\n  ";

    // Print separator line
    for (int i = 0; i < numInputs; i++) std::cout << "------";
    std::cout << "--+";
    for (int i = 0; i < numOutputs; i++) std::cout << "--------";
    std::cout << "\n";

    // Step 3: Iterate through all 2^n combinations
    for (int combo = 0; combo < totalCombinations; combo++) {
        // Set input values using bit manipulation
        // For combo=5 (binary 101) and 3 inputs:
        //   Input 0 gets bit 2 = 1
        //   Input 1 gets bit 1 = 0
        //   Input 2 gets bit 0 = 1
        for (int i = 0; i < numInputs; i++) {
            int bitPosition = numInputs - 1 - i;
            circuit.gates[inputIds[i]].outputValue = (combo >> bitPosition) & 1;
        }

        // Run simulation (silently — no verbose output)
        bool success = simulate(circuit, false);
        if (!success) {
            std::cout << "  [!] Simulation failed. Aborting truth table.\n";
            return;
        }

        // Print this row
        std::cout << "  ";
        for (int i = 0; i < numInputs; i++) {
            std::cout << std::setw(6) << circuit.gates[inputIds[i]].outputValue;
        }
        std::cout << "  |";
        for (int i = 0; i < numOutputs; i++) {
            std::cout << std::setw(8) << circuit.gates[outputIds[i]].outputValue;
        }
        std::cout << "\n";
    }

    std::cout << "  =======================\n";
    std::cout << "  Total rows: " << totalCombinations
              << " (2^" << numInputs << " input combinations)\n";
}

#endif // SIMULATOR_H
