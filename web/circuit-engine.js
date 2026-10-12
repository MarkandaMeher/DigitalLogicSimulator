// =============================================================
// circuit-engine.js — 1:1 Implementation of the C++ Circuit Engine
// =============================================================
// Replicates the exact data structures and algorithms from:
//   • Gate.h       (GateType enum & Gate structure)
//   • Circuit.h    (Directed Acyclic Graph with Adjacency List)
//   • UnionFind.h  (Disjoint Set with Path Compression & Rank)
//   • Simulator.h  (3-Colour DFS, Kahn's Topo Sort, Truth Table)
// =============================================================

// GateType Enum (Matches Gate.h)
const GateType = {
    INPUT:  'INPUT',
    OUTPUT: 'OUTPUT',
    AND:    'AND',
    OR:     'OR',
    NOT:    'NOT',
    XOR:    'XOR',
    NAND:   'NAND',
    NOR:    'NOR',
    XNOR:   'XNOR'
};

// -------------------------------------------------------------
// Disjoint Set / Union-Find (Matches UnionFind.h)
// -------------------------------------------------------------
class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = Array(n).fill(0);
        this.numSets = n;
    }

    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]); // Path compression
        }
        return this.parent[x];
    }

    unite(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);
        if (rootX === rootY) return false;

        // Union by rank
        if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else if (this.rank[rootX] > this.rank[rootY]) {
            this.parent[rootY] = rootX;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }
        this.numSets--;
        return true;
    }

    connected(x, y) {
        return this.find(x) === this.find(y);
    }
}

// -------------------------------------------------------------
// Gate Struct (Matches Gate.h)
// -------------------------------------------------------------
class Gate {
    constructor(id, type, label = '', x = 100, y = 100) {
        this.id = id;
        this.type = type;
        this.label = label || `${type}_${id}`;
        this.inputGateIds = []; // Reverse edges (who feeds this gate)
        this.outputValue = 0;   // 0 or 1
        
        // UI Canvas attributes
        this.x = x;
        this.y = y;
        this.width = (type === GateType.INPUT || type === GateType.OUTPUT) ? 60 : 80;
        this.height = 50;
    }
}

// -------------------------------------------------------------
// Circuit Class (Matches Circuit.h)
// -------------------------------------------------------------
class Circuit {
    constructor() {
        this.gates = [];
        this.adjList = []; // adjList[i] = list of gate IDs driven by gate i
        this.wireNets = null;
    }

    addGate(type, label = '', x = 100, y = 100) {
        const id = this.gates.length;
        const gate = new Gate(id, type, label, x, y);
        this.gates.push(gate);
        this.adjList.push([]);
        return id;
    }

    connect(fromId, toId) {
        if (fromId < 0 || fromId >= this.gates.length ||
            toId < 0 || toId >= this.gates.length) {
            throw new Error(`connect(): Invalid gate ID ${fromId} -> ${toId}`);
        }

        // Avoid duplicate wire
        if (this.adjList[fromId].includes(toId)) {
            return false;
        }

        // Forward edge (adjList) & Reverse edge (inputGateIds)
        this.adjList[fromId].push(toId);
        this.gates[toId].inputGateIds.push(fromId);
        return true;
    }

    disconnect(fromId, toId) {
        if (fromId < 0 || fromId >= this.gates.length ||
            toId < 0 || toId >= this.gates.length) {
            return false;
        }

        this.adjList[fromId] = this.adjList[fromId].filter(id => id !== toId);
        this.gates[toId].inputGateIds = this.gates[toId].inputGateIds.filter(id => id !== fromId);
        return true;
    }

    removeGate(gateId) {
        if (gateId < 0 || gateId >= this.gates.length) return false;
        
        // Remove connections
        for (let i = 0; i < this.gates.length; i++) {
            this.adjList[i] = this.adjList[i].filter(id => id !== gateId);
            this.gates[i].inputGateIds = this.gates[i].inputGateIds.filter(id => id !== gateId);
        }
        
        // Mark as null or reindex
        // To keep IDs stable, we rebuild cleanly:
        const remaining = this.gates.filter(g => g.id !== gateId);
        const oldToNew = {};
        remaining.forEach((g, newIdx) => {
            oldToNew[g.id] = newIdx;
        });

        const newCircuit = new Circuit();
        remaining.forEach(g => {
            newCircuit.addGate(g.type, g.label, g.x, g.y);
            newCircuit.gates[newCircuit.gates.length - 1].outputValue = g.outputValue;
        });

        // Reconnect
        for (let oldFrom = 0; oldFrom < this.adjList.length; oldFrom++) {
            if (oldFrom === gateId) continue;
            for (let oldTo of this.adjList[oldFrom]) {
                if (oldTo === gateId) continue;
                newCircuit.connect(oldToNew[oldFrom], oldToNew[oldTo]);
            }
        }

        this.gates = newCircuit.gates;
        this.adjList = newCircuit.adjList;
        return true;
    }

    toCppCode() {
        let code = `// =============================================================\n`;
        code += `// Generated C++ Circuit Code (Matches Circuit.h)\n`;
        code += `// =============================================================\n`;
        code += `#include "Circuit.h"\n#include "Simulator.h"\n\n`;
        code += `Circuit buildExportedCircuit() {\n`;
        code += `    Circuit circuit;\n\n`;
        code += `    // 1. Add Gates\n`;
        
        this.gates.forEach(g => {
            code += `    int g${g.id} = circuit.addGate(GateType::${g.type}, "${g.label}");\n`;
        });

        code += `\n    // 2. Connect Wires\n`;
        for (let fromId = 0; fromId < this.adjList.length; fromId++) {
            for (let toId of this.adjList[fromId]) {
                code += `    circuit.connect(g${fromId}, g${toId}); // ${this.gates[fromId].label} -> ${this.gates[toId].label}\n`;
            }
        }

        code += `\n    return circuit;\n}\n`;
        return code;
    }
}

// -------------------------------------------------------------
// Algorithms Module (Matches Simulator.h)
// -------------------------------------------------------------

// Tarjan's 3-Colour DFS Cycle Detection
function hasCycleDFS(node, color, circuit, cyclePath = []) {
    color[node] = 1; // GRAY
    cyclePath.push(node);

    for (let neighbor of circuit.adjList[node]) {
        if (color[neighbor] === 1) {
            // Found back edge
            cyclePath.push(neighbor);
            return { hasCycle: true, cycleNodes: [...cyclePath] };
        }
        if (color[neighbor] === 0) {
            const res = hasCycleDFS(neighbor, color, circuit, cyclePath);
            if (res.hasCycle) return res;
        }
    }

    cyclePath.pop();
    color[node] = 2; // BLACK
    return { hasCycle: false, cycleNodes: [] };
}

function checkCycle(circuit) {
    const n = circuit.gates.length;
    if (n === 0) return { hasCycle: false, cycleNodes: [] };

    const color = Array(n).fill(0); // 0 = WHITE
    for (let i = 0; i < n; i++) {
        if (color[i] === 0) {
            const res = hasCycleDFS(i, color, circuit, []);
            if (res.hasCycle) return res;
        }
    }
    return { hasCycle: false, cycleNodes: [] };
}

// Kahn's BFS Topological Sort Algorithm
function topologicalSort(circuit) {
    const n = circuit.gates.length;
    const inDegree = Array(n).fill(0);

    for (let i = 0; i < n; i++) {
        for (let neighbor of circuit.adjList[i]) {
            inDegree[neighbor]++;
        }
    }

    const queue = [];
    for (let i = 0; i < n; i++) {
        if (inDegree[i] === 0) {
            queue.push(i);
        }
    }

    const order = [];
    while (queue.length > 0) {
        const curr = queue.shift();
        order.push(curr);

        for (let neighbor of circuit.adjList[curr]) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] === 0) {
                queue.push(neighbor);
            }
        }
    }

    return order;
}

// Gate Boolean Logic Evaluation (Matches evaluateGate in Simulator.h)
function evaluateGate(gate, allGates) {
    switch (gate.type) {
        case GateType.AND: {
            let res = 1;
            for (let inId of gate.inputGateIds) {
                res &= allGates[inId].outputValue;
            }
            gate.outputValue = res;
            break;
        }
        case GateType.OR: {
            let res = 0;
            for (let inId of gate.inputGateIds) {
                res |= allGates[inId].outputValue;
            }
            gate.outputValue = res;
            break;
        }
        case GateType.NOT: {
            if (gate.inputGateIds.length > 0) {
                gate.outputValue = allGates[gate.inputGateIds[0]].outputValue ? 0 : 1;
            }
            break;
        }
        case GateType.XOR: {
            let res = 0;
            for (let inId of gate.inputGateIds) {
                res ^= allGates[inId].outputValue;
            }
            gate.outputValue = res;
            break;
        }
        case GateType.NAND: {
            let res = 1;
            for (let inId of gate.inputGateIds) {
                res &= allGates[inId].outputValue;
            }
            gate.outputValue = res === 1 ? 0 : 1;
            break;
        }
        case GateType.NOR: {
            let res = 0;
            for (let inId of gate.inputGateIds) {
                res |= allGates[inId].outputValue;
            }
            gate.outputValue = res === 1 ? 0 : 1;
            break;
        }
        case GateType.XNOR: {
            let res = 0;
            for (let inId of gate.inputGateIds) {
                res ^= allGates[inId].outputValue;
            }
            gate.outputValue = res === 1 ? 0 : 1;
            break;
        }
        case GateType.OUTPUT: {
            if (gate.inputGateIds.length > 0) {
                gate.outputValue = allGates[gate.inputGateIds[0]].outputValue;
            }
            break;
        }
        case GateType.INPUT:
            // Keeps user-set value
            break;
    }
}

// Full Simulation Pipeline
function simulateCircuit(circuit) {
    if (circuit.gates.length === 0) {
        return { success: false, message: 'Circuit is empty.' };
    }

    // 1. Cycle Check
    const cycleRes = checkCycle(circuit);
    if (cycleRes.hasCycle) {
        return {
            success: false,
            hasCycle: true,
            cycleNodes: cycleRes.cycleNodes,
            message: `Feedback loop (cycle) detected involving Gate ID: ${cycleRes.cycleNodes.join(' -> ')}`
        };
    }

    // 2. Topological Sort
    const order = topologicalSort(circuit);

    // 3. Step-by-Step Evaluation Trace
    const trace = [];
    for (let gateId of order) {
        const g = circuit.gates[gateId];
        evaluateGate(g, circuit.gates);
        trace.push({
            gateId: g.id,
            label: g.label,
            type: g.type,
            outputValue: g.outputValue,
            inputs: g.inputGateIds.map(inId => ({
                id: inId,
                label: circuit.gates[inId].label,
                val: circuit.gates[inId].outputValue
            }))
        });
    }

    return {
        success: true,
        order: order,
        trace: trace
    };
}

// Exhaustive Truth Table Generator (All 2^N Combinations)
function generateTruthTableJS(circuit) {
    const inputGates = circuit.gates.filter(g => g.type === GateType.INPUT);
    const outputGates = circuit.gates.filter(g => g.type === GateType.OUTPUT);

    if (inputGates.length === 0 || outputGates.length === 0) {
        return { success: false, message: 'Circuit must have at least 1 INPUT and 1 OUTPUT gate.' };
    }

    const n = inputGates.length;
    if (n > 12) {
        return { success: false, message: `Too many inputs (${n}). Browser limit is 12 inputs (4096 rows).` };
    }

    const totalRows = 1 << n;
    const tableData = [];

    // Save current states
    const savedInputs = inputGates.map(g => g.outputValue);

    for (let combo = 0; combo < totalRows; combo++) {
        const inputVals = [];
        for (let i = 0; i < n; i++) {
            const bitPos = n - 1 - i;
            const val = (combo >> bitPos) & 1;
            inputGates[i].outputValue = val;
            inputVals.push(val);
        }

        const simRes = simulateCircuit(circuit);
        if (!simRes.success) {
            return { success: false, message: simRes.message };
        }

        const outputVals = outputGates.map(g => g.outputValue);
        tableData.push({ inputs: inputVals, outputs: outputVals });
    }

    // Restore input states
    inputGates.forEach((g, i) => g.outputValue = savedInputs[i]);
    simulateCircuit(circuit);

    return {
        success: true,
        inputs: inputGates.map(g => g.label),
        outputs: outputGates.map(g => g.label),
        rows: tableData
    };
}
