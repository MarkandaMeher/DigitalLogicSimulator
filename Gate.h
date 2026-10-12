// =============================================================
// Gate.h — Defines the GateType enum and Gate struct
// =============================================================
// Each gate is a NODE in our circuit DAG.
// It knows its type, its unique id, which gates feed into it,
// and its current output value.
// =============================================================

#ifndef GATE_H
#define GATE_H

#include <vector>
#include <string>

// -------------------------------------------------------------
// GateType: Every node in the circuit is one of these types.
//
//   INPUT  — A primary input (user sets its value to 0 or 1)
//   OUTPUT — A primary output (displays a result)
//   AND    — Outputs 1 only if ALL inputs are 1
//   OR     — Outputs 1 if ANY input is 1
//   NOT    — Inverts a single input (1→0, 0→1)
//   XOR    — Outputs 1 if an ODD number of inputs are 1
// -------------------------------------------------------------
enum class GateType {
    INPUT,
    OUTPUT,
    AND,
    OR,
    NOT,
    XOR,
    NAND,
    NOR,
    XNOR
};

// Helper: Convert GateType to a human-readable string
inline std::string gateTypeToString(GateType type) {
    switch (type) {
        case GateType::INPUT:  return "INPUT";
        case GateType::OUTPUT: return "OUTPUT";
        case GateType::AND:    return "AND";
        case GateType::OR:     return "OR";
        case GateType::NOT:    return "NOT";
        case GateType::XOR:    return "XOR";
        case GateType::NAND:   return "NAND";
        case GateType::NOR:    return "NOR";
        case GateType::XNOR:   return "XNOR";
        default:               return "UNKNOWN";
    }
}

// -------------------------------------------------------------
// Gate: A single node in the circuit DAG.
//
//   id            — Unique integer index (position in Circuit's
//                   gate vector and adjacency list)
//   type          — What kind of gate this is
//   label         — Optional human-readable name (e.g., "A", "B")
//   inputGateIds  — IDs of gates whose outputs feed INTO this
//                   gate's inputs (reverse edges for evaluation)
//   outputValue   — The gate's current computed output (0 or 1)
// -------------------------------------------------------------
struct Gate {
    int         id;
    GateType    type;
    std::string label;

    // Which gates feed INTO this gate (used during evaluation)
    std::vector<int> inputGateIds;

    // Current output value of this gate (0 or 1)
    int outputValue;

    // Constructor with sensible defaults
    Gate(int id, GateType type, const std::string& label = "")
        : id(id), type(type), label(label), outputValue(0) {}
};

#endif // GATE_H
