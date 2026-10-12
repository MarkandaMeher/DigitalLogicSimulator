// =============================================================
// app.js — Interactive Canvas UI & Controller for Circuit Simulator
// =============================================================

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('circuitCanvas');
    const ctx = canvas.getContext('2d');
    const wrapper = document.getElementById('canvasWrapper');

    // High-DPI canvas resizing
    function resizeCanvas() {
        canvas.width = wrapper.clientWidth;
        canvas.height = wrapper.clientHeight;
        render();
    }
    window.addEventListener('resize', resizeCanvas);

    // Core Circuit Model
    let circuit = new Circuit();

    // UI State
    let selectedGateId = null;
    let draggingGate = null;
    let dragOffset = { x: 0, y: 0 };
    let connectingWire = null; // { fromId, startX, startY, currentX, currentY }
    let stepAnimationActive = false;
    let highlightedStepGate = null;

    // ---------------------------------------------------------
    // Port Coordinates Calculation
    // ---------------------------------------------------------
    function getPorts(gate) {
        const inPorts = [];
        const outPorts = [];

        if (gate.type === GateType.INPUT) {
            // Output port on right
            outPorts.push({ x: gate.x + gate.width, y: gate.y + gate.height / 2 });
        } else if (gate.type === GateType.OUTPUT) {
            // Input port on left
            inPorts.push({ x: gate.x, y: gate.y + gate.height / 2 });
        } else if (gate.type === GateType.NOT) {
            // 1 input, 1 output
            inPorts.push({ x: gate.x, y: gate.y + gate.height / 2 });
            outPorts.push({ x: gate.x + gate.width, y: gate.y + gate.height / 2 });
        } else {
            // Multi-input gates (e.g. 2 inputs on left, 1 output on right)
            inPorts.push({ x: gate.x, y: gate.y + 16 });
            inPorts.push({ x: gate.x, y: gate.y + gate.height - 16 });
            outPorts.push({ x: gate.x + gate.width, y: gate.y + gate.height / 2 });
        }

        return { inPorts, outPorts };
    }

    // ---------------------------------------------------------
    // Canvas Drawing Routines
    // ---------------------------------------------------------
    function drawGrid() {
        const gridSize = 24;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
        ctx.lineWidth = 1;

        ctx.beginPath();
        for (let x = 0; x < canvas.width; x += gridSize) {
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
        }
        for (let y = 0; y < canvas.height; y += gridSize) {
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
        }
        ctx.stroke();
    }

    function drawWire(x1, y1, x2, y2, isHigh, isCycle = false) {
        ctx.save();
        ctx.beginPath();
        
        // Cubic Bezier curve for natural wire bend
        const dx = Math.abs(x2 - x1) * 0.5 + 20;
        ctx.moveTo(x1, y1);
        ctx.bezierCurveTo(x1 + dx, y1, x2 - dx, y2, x2, y2);

        if (isCycle) {
            ctx.strokeStyle = '#e94560';
            ctx.lineWidth = 3;
            ctx.shadowColor = '#e94560';
            ctx.shadowBlur = 8;
        } else if (isHigh) {
            ctx.strokeStyle = '#10b981';
            ctx.lineWidth = 3;
            ctx.shadowColor = '#10b981';
            ctx.shadowBlur = 6;
        } else {
            ctx.strokeStyle = '#475569';
            ctx.lineWidth = 2;
            ctx.shadowBlur = 0;
        }

        ctx.stroke();
        ctx.restore();
    }

    function drawGate(gate) {
        const isSelected = (gate.id === selectedGateId);
        const isHighlighted = (gate.id === highlightedStepGate);
        const { inPorts, outPorts } = getPorts(gate);

        ctx.save();

        // Highlighting / Selection Glow
        if (isHighlighted) {
            ctx.shadowColor = '#fbbf24';
            ctx.shadowBlur = 18;
            ctx.strokeStyle = '#fbbf24';
            ctx.lineWidth = 3;
        } else if (isSelected) {
            ctx.shadowColor = '#3b82f6';
            ctx.shadowBlur = 12;
            ctx.strokeStyle = '#3b82f6';
            ctx.lineWidth = 2;
        } else {
            ctx.strokeStyle = '#27374d';
            ctx.lineWidth = 1.5;
            ctx.shadowBlur = 0;
        }

        // Gate Box Body
        ctx.fillStyle = '#1c2738';
        ctx.beginPath();
        ctx.roundRect(gate.x, gate.y, gate.width, gate.height, 8);
        ctx.fill();
        ctx.stroke();

        // Gate Type & Label Text
        ctx.font = 'bold 12px "Segoe UI", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        if (gate.type === GateType.INPUT) {
            // Toggle Switch Style
            ctx.fillStyle = gate.outputValue === 1 ? '#10b981' : '#64748b';
            ctx.fillText(gate.label, gate.x + gate.width / 2, gate.y + 16);
            
            // Value Badge
            ctx.fillStyle = gate.outputValue === 1 ? '#059669' : '#334155';
            ctx.beginPath();
            ctx.roundRect(gate.x + 12, gate.y + 26, gate.width - 24, 16, 4);
            ctx.fill();
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 11px monospace';
            ctx.fillText(gate.outputValue === 1 ? '1 [ON]' : '0 [OFF]', gate.x + gate.width / 2, gate.y + 34);

        } else if (gate.type === GateType.OUTPUT) {
            // Bulb Indicator Style
            ctx.fillStyle = gate.outputValue === 1 ? '#f59e0b' : '#64748b';
            ctx.fillText(gate.label, gate.x + gate.width / 2, gate.y + 16);

            // Glowing Bulb Circle
            ctx.beginPath();
            ctx.arc(gate.x + gate.width / 2, gate.y + 34, 7, 0, Math.PI * 2);
            if (gate.outputValue === 1) {
                ctx.fillStyle = '#fbbf24';
                ctx.shadowColor = '#fbbf24';
                ctx.shadowBlur = 10;
            } else {
                ctx.fillStyle = '#334155';
                ctx.shadowBlur = 0;
            }
            ctx.fill();

        } else {
            // Logic Gate Body
            ctx.fillStyle = '#e2e8f0';
            ctx.fillText(gate.type, gate.x + gate.width / 2, gate.y + 18);

            ctx.font = '10px "Segoe UI", sans-serif';
            ctx.fillStyle = '#94a3b8';
            ctx.fillText(gate.label, gate.x + gate.width / 2, gate.y + 34);
        }

        // Draw Input Ports (Left)
        inPorts.forEach(port => {
            ctx.beginPath();
            ctx.arc(port.x, port.y, 4.5, 0, Math.PI * 2);
            ctx.fillStyle = '#3b82f6';
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 1;
            ctx.stroke();
        });

        // Draw Output Ports (Right)
        outPorts.forEach(port => {
            ctx.beginPath();
            ctx.arc(port.x, port.y, 5, 0, Math.PI * 2);
            ctx.fillStyle = gate.outputValue === 1 ? '#10b981' : '#64748b';
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 1;
            ctx.stroke();
        });

        ctx.restore();
    }

    // ---------------------------------------------------------
    // Main Render Loop
    // ---------------------------------------------------------
    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid();

        // Check for cycles for visual highlighting
        const cycleInfo = checkCycle(circuit);

        // 1. Draw All Established Wires
        for (let fromId = 0; fromId < circuit.adjList.length; fromId++) {
            const fromGate = circuit.gates[fromId];
            if (!fromGate) continue;
            const { outPorts } = getPorts(fromGate);
            const startPort = outPorts[0];

            for (let toId of circuit.adjList[fromId]) {
                const toGate = circuit.gates[toId];
                if (!toGate) continue;
                const { inPorts } = getPorts(toGate);
                
                // Route to appropriate input port
                const portIndex = toGate.inputGateIds.indexOf(fromId) % inPorts.length;
                const endPort = inPorts[portIndex] || inPorts[0];

                const isCycleWire = cycleInfo.hasCycle &&
                    cycleInfo.cycleNodes.includes(fromId) &&
                    cycleInfo.cycleNodes.includes(toId);

                drawWire(startPort.x, startPort.y, endPort.x, endPort.y, fromGate.outputValue === 1, isCycleWire);
            }
        }

        // 2. Draw Wire Currently Being Drawn
        if (connectingWire) {
            drawWire(connectingWire.startX, connectingWire.startY, connectingWire.currentX, connectingWire.currentY, false);
        }

        // 3. Draw All Gates
        circuit.gates.forEach(gate => drawGate(gate));

        // Update UI Diagnostics
        updateUI(cycleInfo);
    }

    // ---------------------------------------------------------
    // Diagnostics & Inspector Update
    // ---------------------------------------------------------
    function updateUI(cycleInfo) {
        // Status Bar
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('circuitStatusText');
        const nodeWireCount = document.getElementById('nodeWireCount');

        let wireCount = 0;
        circuit.adjList.forEach(list => wireCount += list.length);
        nodeWireCount.textContent = `Gates: ${circuit.gates.length} | Wires: ${wireCount}`;

        if (cycleInfo.hasCycle) {
            statusDot.className = 'dot cycle';
            statusText.textContent = `Cycle Detected: ${cycleInfo.cycleNodes.join(' -> ')}`;
            statusText.style.color = '#e94560';
        } else {
            statusDot.className = 'dot';
            statusText.textContent = 'Acyclic DAG (Ready)';
            statusText.style.color = '#10b981';
        }

        // Inspector Panel
        const inspector = document.getElementById('inspectorDetails');
        if (selectedGateId !== null && circuit.gates[selectedGateId]) {
            const g = circuit.gates[selectedGateId];
            inspector.innerHTML = `
                <div class="info-row"><span class="info-label">Gate ID:</span><span class="info-val">${g.id}</span></div>
                <div class="info-row"><span class="info-label">Type:</span><span class="info-val">${g.type}</span></div>
                <div class="info-row"><span class="info-label">Label:</span><span class="info-val">"${g.label}"</span></div>
                <div class="info-row"><span class="info-label">Output State:</span><span class="info-val" style="color:${g.outputValue === 1 ? '#10b981' : '#94a3b8'};">${g.outputValue} (${g.outputValue === 1 ? 'HIGH' : 'LOW'})</span></div>
                <div style="margin-top: 8px; font-weight: 600; color: #94a3b8;">Fan-In (Driven by):</div>
                <div style="font-size: 11px; color: #fff; margin-bottom: 6px;">
                    ${g.inputGateIds.length === 0 ? '(None / User Input)' : g.inputGateIds.map(id => `• Gate ${id} [${circuit.gates[id].label}] = ${circuit.gates[id].outputValue}`).join('<br>')}
                </div>
                <div style="font-weight: 600; color: #94a3b8;">Fan-Out (Drives):</div>
                <div style="font-size: 11px; color: #fff;">
                    ${circuit.adjList[g.id].length === 0 ? '(None / Output Pin)' : circuit.adjList[g.id].map(id => `• Gate ${id} [${circuit.gates[id].label}]`).join('<br>')}
                </div>
            `;
        } else {
            inspector.innerHTML = `<p style="color: var(--text-muted); font-size: 11.5px;">Click any gate on the canvas to inspect its fan-in wires, logic equation, and live signal.</p>`;
        }

        // 3-Stage Pipeline Summary
        const inGates = circuit.gates.filter(g => g.type === GateType.INPUT).map(g => `${g.label}=${g.outputValue}`);
        const logicGates = circuit.gates.filter(g => g.type !== GateType.INPUT && g.type !== GateType.OUTPUT).map(g => `${g.label}=${g.outputValue}`);
        const outGates = circuit.gates.filter(g => g.type === GateType.OUTPUT).map(g => `${g.label}=${g.outputValue}`);

        document.getElementById('pipelineInputs').textContent = inGates.length > 0 ? inGates.join(', ') : 'None';
        document.getElementById('pipelineLogic').textContent = logicGates.length > 0 ? logicGates.join(', ') : 'None';
        document.getElementById('pipelineOutputs').textContent = outGates.length > 0 ? outGates.join(', ') : 'None';
    }

    // ---------------------------------------------------------
    // Hit Testing Helpers
    // ---------------------------------------------------------
    function getGateAt(x, y) {
        for (let i = circuit.gates.length - 1; i >= 0; i--) {
            const g = circuit.gates[i];
            if (x >= g.x && x <= g.x + g.width && y >= g.y && y <= g.y + g.height) {
                return g;
            }
        }
        return null;
    }

    function getPortAt(x, y) {
        for (let g of circuit.gates) {
            const { inPorts, outPorts } = getPorts(g);
            
            // Check Output Ports
            for (let p of outPorts) {
                if (Math.hypot(p.x - x, p.y - y) <= 12) {
                    return { gate: g, type: 'output', port: p };
                }
            }

            // Check Input Ports
            for (let i = 0; i < inPorts.length; i++) {
                const p = inPorts[i];
                if (Math.hypot(p.x - x, p.y - y) <= 12) {
                    return { gate: g, type: 'input', port: p, index: i };
                }
            }
        }
        return null;
    }

    // ---------------------------------------------------------
    // Mouse Event Handlers (Drag, Wire Drawing, Click)
    // ---------------------------------------------------------
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // 1. Check if clicking on an output port to start a wire
        const portHit = getPortAt(x, y);
        if (portHit && portHit.type === 'output') {
            connectingWire = {
                fromId: portHit.gate.id,
                startX: portHit.port.x,
                startY: portHit.port.y,
                currentX: x,
                currentY: y
            };
            return;
        }

        // 2. Check if clicking on a gate
        const gateHit = getGateAt(x, y);
        if (gateHit) {
            selectedGateId = gateHit.id;

            // If clicking INPUT pin, toggle its value immediately!
            if (gateHit.type === GateType.INPUT && x < gateHit.x + gateHit.width - 10) {
                gateHit.outputValue = (gateHit.outputValue === 1 ? 0 : 1);
                simulateCircuit(circuit);
                render();
                return;
            }

            // Start dragging gate
            draggingGate = gateHit;
            dragOffset.x = x - gateHit.x;
            dragOffset.y = y - gateHit.y;
            render();
            return;
        }

        // Click on blank canvas deselects
        selectedGateId = null;
        render();
    });

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (connectingWire) {
            connectingWire.currentX = x;
            connectingWire.currentY = y;
            render();
            return;
        }

        if (draggingGate) {
            draggingGate.x = Math.max(10, Math.min(canvas.width - draggingGate.width - 10, x - dragOffset.x));
            draggingGate.y = Math.max(10, Math.min(canvas.height - draggingGate.height - 10, y - dragOffset.y));
            render();
            return;
        }
    });

    canvas.addEventListener('mouseup', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (connectingWire) {
            const portHit = getPortAt(x, y);
            if (portHit && portHit.type === 'input' && portHit.gate.id !== connectingWire.fromId) {
                // Connect wire
                circuit.connect(connectingWire.fromId, portHit.gate.id);
                simulateCircuit(circuit);
            }
            connectingWire = null;
            render();
        }

        draggingGate = null;
    });

    // Keyboard controls (Delete / Backspace to remove selected gate)
    window.addEventListener('keydown', (e) => {
        if ((e.key === 'Delete' || e.key === 'Backspace') && selectedGateId !== null) {
            circuit.removeGate(selectedGateId);
            selectedGateId = null;
            simulateCircuit(circuit);
            render();
        }
    });

    // ---------------------------------------------------------
    // HTML5 Drag & Drop from Left Palette to Canvas
    // ---------------------------------------------------------
    const paletteCards = document.querySelectorAll('.gate-card');
    paletteCards.forEach(card => {
        card.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('gateType', card.dataset.type);
        });
    });

    wrapper.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
    });

    wrapper.addEventListener('drop', (e) => {
        e.preventDefault();
        const gateType = e.dataTransfer.getData('gateType');
        if (!gateType) return;

        const rect = canvas.getBoundingClientRect();
        const x = Math.max(20, e.clientX - rect.left - 40);
        const y = Math.max(20, e.clientY - rect.top - 25);

        const newId = circuit.addGate(gateType, `${gateType}_${circuit.gates.length}`, x, y);
        selectedGateId = newId;
        simulateCircuit(circuit);
        render();
    });

    // ---------------------------------------------------------
    // Action Buttons Handlers
    // ---------------------------------------------------------

    // 1. Run Simulation
    document.getElementById('btnSimulate').addEventListener('click', () => {
        const res = simulateCircuit(circuit);
        if (!res.success) {
            alert(res.message);
        } else {
            document.getElementById('topoOrderBox').textContent =
                res.order.map(id => `G${id}[${circuit.gates[id].label}]`).join(' -> ');
        }
        render();
    });

    // 2. Step-by-Step Kahn's Topological Animation
    document.getElementById('btnStepTopo').addEventListener('click', async () => {
        const res = simulateCircuit(circuit);
        if (!res.success) {
            alert(res.message);
            return;
        }

        const topoBox = document.getElementById('topoOrderBox');
        topoBox.textContent = 'Topological Execution Trace:\n';

        for (let i = 0; i < res.order.length; i++) {
            const gateId = res.order[i];
            highlightedStepGate = gateId;
            render();

            const g = circuit.gates[gateId];
            topoBox.textContent += `[Step ${i+1}/${res.order.length}] G${gateId} [${g.type}: ${g.label}] = ${g.outputValue}\n`;
            topoBox.scrollTop = topoBox.scrollHeight;

            await new Promise(r => setTimeout(r, 600));
        }

        highlightedStepGate = null;
        render();
    });

    // 3. Clear Canvas
    document.getElementById('btnClear').addEventListener('click', () => {
        if (confirm('Clear the entire circuit canvas?')) {
            circuit = new Circuit();
            selectedGateId = null;
            render();
        }
    });

    // 4. Truth Table Modal
    const modalTruthTable = document.getElementById('modalTruthTable');
    document.getElementById('btnTruthTable').addEventListener('click', () => {
        const tt = generateTruthTableJS(circuit);
        if (!tt.success) {
            alert(tt.message);
            return;
        }

        document.getElementById('ttCombinations').textContent = tt.rows.length;
        const container = document.getElementById('truthTableContainer');
        
        let html = '<table class="truth-table"><thead><tr>';
        tt.inputs.forEach(inName => html += `<th>INPUT: ${inName}</th>`);
        tt.outputs.forEach(outName => html += `<th style="background-color:#1e3a5f;">OUTPUT: ${outName}</th>`);
        html += '</tr></thead><tbody>';

        tt.rows.forEach(r => {
            html += '<tr>';
            r.inputs.forEach(v => html += `<td class="${v === 1 ? 'high' : 'low'}">${v}</td>`);
            r.outputs.forEach(v => html += `<td class="${v === 1 ? 'high' : 'low'}" style="font-weight:bold;">${v}</td>`);
            html += '</tr>';
        });

        html += '</tbody></table>';
        container.innerHTML = html;
        modalTruthTable.classList.add('active');
    });

    document.getElementById('closeTruthTable').addEventListener('click', () => modalTruthTable.classList.remove('active'));
    document.getElementById('closeTruthTableBtn').addEventListener('click', () => modalTruthTable.classList.remove('active'));

    // 5. C++ Code Modal
    const modalCppSync = document.getElementById('modalCppSync');
    document.getElementById('btnExportCpp').addEventListener('click', () => {
        document.getElementById('cppCodeDisplay').textContent = circuit.toCppCode();
        modalCppSync.classList.add('active');
    });

    document.getElementById('closeCppSync').addEventListener('click', () => modalCppSync.classList.remove('active'));
    document.getElementById('closeCppSyncBtn').addEventListener('click', () => modalCppSync.classList.remove('active'));

    document.getElementById('btnCopyCpp').addEventListener('click', () => {
        navigator.clipboard.writeText(circuit.toCppCode()).then(() => {
            alert('C++ circuit code copied to clipboard! Matches Circuit.h and Simulator.h.');
        });
    });

    // ---------------------------------------------------------
    // Preset Circuit Loaders
    // ---------------------------------------------------------

    // Preset 1: Half Adder
    document.getElementById('presetHalfAdder').addEventListener('click', () => {
        circuit = new Circuit();
        const inA = circuit.addGate(GateType.INPUT, 'A', 80, 100);
        const inB = circuit.addGate(GateType.INPUT, 'B', 80, 220);
        const xorG = circuit.addGate(GateType.XOR, 'XOR1', 250, 90);
        const andG = circuit.addGate(GateType.AND, 'AND1', 250, 230);
        const sumOut = circuit.addGate(GateType.OUTPUT, 'Sum', 430, 90);
        const carryOut = circuit.addGate(GateType.OUTPUT, 'Carry', 430, 230);

        circuit.connect(inA, xorG);
        circuit.connect(inB, xorG);
        circuit.connect(inA, andG);
        circuit.connect(inB, andG);
        circuit.connect(xorG, sumOut);
        circuit.connect(andG, carryOut);

        circuit.gates[inA].outputValue = 1;
        circuit.gates[inB].outputValue = 0;
        simulateCircuit(circuit);
        render();
    });

    // Preset 2: NOR Circuit
    document.getElementById('presetNOR').addEventListener('click', () => {
        circuit = new Circuit();
        const inA = circuit.addGate(GateType.INPUT, 'A', 80, 120);
        const inB = circuit.addGate(GateType.INPUT, 'B', 80, 240);
        const orG = circuit.addGate(GateType.OR, 'OR1', 250, 180);
        const notG = circuit.addGate(GateType.NOT, 'NOT1', 390, 180);
        const outY = circuit.addGate(GateType.OUTPUT, 'Y', 530, 180);

        circuit.connect(inA, orG);
        circuit.connect(inB, orG);
        circuit.connect(orG, notG);
        circuit.connect(notG, outY);

        simulateCircuit(circuit);
        render();
    });

    // Preset 3: 2-to-1 Multiplexer
    document.getElementById('presetMux').addEventListener('click', () => {
        circuit = new Circuit();
        const inA = circuit.addGate(GateType.INPUT, 'A', 80, 80);
        const inB = circuit.addGate(GateType.INPUT, 'B', 80, 320);
        const inS = circuit.addGate(GateType.INPUT, 'Sel', 80, 200);

        const notS = circuit.addGate(GateType.NOT, 'NOT_S', 220, 140);
        const and1 = circuit.addGate(GateType.AND, 'AND1', 360, 90);
        const and2 = circuit.addGate(GateType.AND, 'AND2', 360, 270);
        const orG = circuit.addGate(GateType.OR, 'OR1', 490, 180);
        const outY = circuit.addGate(GateType.OUTPUT, 'Y', 620, 180);

        circuit.connect(inS, notS);
        circuit.connect(inA, and1);
        circuit.connect(notS, and1);
        circuit.connect(inB, and2);
        circuit.connect(inS, and2);
        circuit.connect(and1, orG);
        circuit.connect(and2, orG);
        circuit.connect(orG, outY);

        circuit.gates[inA].outputValue = 1;
        simulateCircuit(circuit);
        render();
    });

    // Preset 4: IEEE ISCAS '85 c17 Benchmark
    document.getElementById('presetISCAS').addEventListener('click', () => {
        circuit = new Circuit();
        const in1 = circuit.addGate(GateType.INPUT, 'N1', 60, 60);
        const in2 = circuit.addGate(GateType.INPUT, 'N2', 60, 140);
        const in3 = circuit.addGate(GateType.INPUT, 'N3', 60, 220);
        const in6 = circuit.addGate(GateType.INPUT, 'N6', 60, 300);
        const in7 = circuit.addGate(GateType.INPUT, 'N7', 60, 380);

        const g10 = circuit.addGate(GateType.NAND, 'G10', 220, 80);
        const g11 = circuit.addGate(GateType.NAND, 'G11', 220, 260);
        const g16 = circuit.addGate(GateType.NAND, 'G16', 360, 160);
        const g19 = circuit.addGate(GateType.NAND, 'G19', 360, 340);
        const g22 = circuit.addGate(GateType.NAND, 'G22', 500, 100);
        const g23 = circuit.addGate(GateType.NAND, 'G23', 500, 240);

        const out22 = circuit.addGate(GateType.OUTPUT, 'N22', 640, 100);
        const out23 = circuit.addGate(GateType.OUTPUT, 'N23', 640, 240);

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

        simulateCircuit(circuit);
        render();
    });

    // Initial Setup: Resize & Load Half Adder preset
    resizeCanvas();
    document.getElementById('presetHalfAdder').click();
});
