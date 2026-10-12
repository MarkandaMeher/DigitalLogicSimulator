import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_short_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY_DARK = RGBColor(15, 52, 96)       # #0F3460
    C_CORAL = RGBColor(233, 69, 96)          # #E94560
    C_PURPLE = RGBColor(83, 52, 131)         # #533483
    C_EMERALD = RGBColor(39, 174, 96)        # #27AE60
    C_CARD_BG = RGBColor(240, 243, 246)      # #F0F3F6
    C_WHITE = RGBColor(255, 255, 255)
    C_TEXT_DARK = RGBColor(26, 26, 46)       # #1A1A2E
    C_TEXT_MUTED = RGBColor(100, 110, 125)
    C_BORDER = RGBColor(220, 224, 230)

    def add_header(slide, title_text, slide_num):
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_CORAL
        top_bar.line.color.rgb = C_CORAL

        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.9))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = f"FIRST REVIEW — OCTOBER 12, 2026 | SLIDE {slide_num} OF 9"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CORAL
        p_cat.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK

        foot_bar = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf_f = foot_bar.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p_foot = tf_f.paragraphs[0]
        p_foot.text = "Digital Logic Circuit Simulator | Team: Markanda Meher (206126020) & Nikhil (206126021) | Dept. of CSE"
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = C_TEXT_MUTED

    def create_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (1/9)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.color.rgb = C_NAVY_DARK

    acc = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.18))
    acc.fill.solid()
    acc.fill.fore_color.rgb = C_CORAL
    acc.line.color.rgb = C_CORAL

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(10.9), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "ADVANCED DATA STRUCTURES & ALGORITHMS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Digital Logic Circuit Simulator"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Graph-Theoretic Logic Simulation, Cycle Detection & Interactive EDA System"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(210, 225, 245)
    p.space_after = Pt(26)

    p = tf1.add_paragraph()
    p.text = "━" * 46
    p.font.size = Pt(12)
    p.font.color.rgb = C_PURPLE
    p.space_after = Pt(22)

    p = tf1.add_paragraph()
    p.text = "Team Members:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    p = tf1.add_paragraph()
    p.text = "• Markanda Meher  —  Roll No. 206126020\n• Nikhil                    —  Roll No. 206126021"
    p.font.size = Pt(14)
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(18)

    p = tf1.add_paragraph()
    p.text = "First Review — October 12, 2026 (Presentation: 9 Slides Concise Format)"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(180, 195, 215)

    # =========================================================================
    # SLIDE 2: 1. Introduction - Problem Statement & Motivation (2/9)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Introduction — Problem Statement & Need to be Solved", 2)

    create_card(s2, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb = s2.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.2), Inches(4.85))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Problem: Physical Hardware Bottlenecks"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(12)

    p_items = [
        ("Fragile Connections & Wire Clutter: ", "Physical breadboards suffer from loose jumper contacts, pin damage, and wiring complexity that obscures circuit logic."),
        ("No Pre-Simulation Safety: ", "Accidental feedback loops or short circuits cause permanent component burnouts with no diagnostic warnings."),
        ("High Lab Cost: ", "Oscilloscopes, logic analyzers, and discrete IC inventories require recurring institutional expenses and lack remote access."),
        ("Opaque Internal States: ", "Physically probing dozens of internal nodes simultaneously is cumbersome without software visualization.")
    ]
    for h, b in p_items:
        p = tf.add_paragraph()
        p.text = "• " + h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY_DARK
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = "  " + b
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_after = Pt(8)

    create_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb2 = s2.shapes.add_textbox(Inches(7.05), Inches(1.65), Inches(5.2), Inches(4.85))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "The Solution & Need to be Solved"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(12)

    s_items = [
        ("Graph-Theoretic Software Modeling: ", "Models digital circuits strictly as Directed Acyclic Graphs (DAGs) with mathematical evaluation guarantees."),
        ("Algorithmic Pre-Validation: ", "Runs Tarjan's 3-colour DFS to detect circular feedback loops BEFORE simulation, preventing infinite execution loops."),
        ("Topological Gate Scheduling: ", "Applies Kahn's BFS algorithm to determine the exact computation order so gate inputs are always ready before evaluation."),
        ("Dual Architecture: ", "Features a zero-dependency high-speed C++17 core engine paired with a modern drag-and-drop web EDA canvas.")
    ]
    for h, b in s_items:
        p = tf2.add_paragraph()
        p.text = "• " + h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_CORAL
        p.space_after = Pt(2)
        p2 = tf2.add_paragraph()
        p2.text = "  " + b
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: 2. Literature Survey — 3 Research Papers Analyzed (3/9)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Literature Survey — Analysis of 3 Papers & Drawbacks", 3)

    papers = [
        ("Paper 1: Kahn's Topological Sort (1962)", "A. B. Kahn — Communications of the ACM, Vol. 5, No. 11, pp. 558–562",
         "Introduced in-degree BFS queue algorithm for ordering DAGs in O(V + E) time. Used in our simulator for dependency-ordered gate calculation.",
         "Drawbacks: (1) Silent failure on cycles (stops when queue empties without identifying offending nodes); (2) Arbitrary tie-breaking ignoring critical paths; (3) Static only (must re-sort entire graph on wire changes)."),
        ("Paper 2: Tarjan's DFS Framework (1972)", "Robert E. Tarjan — SIAM Journal on Computing, Vol. 1, No. 2, pp. 146–160",
         "Established linear-time O(V + E) DFS graph traversal with back-edge classification. Used in our simulator for 3-colour cycle pre-validation.",
         "Drawbacks: (1) Recursive stack overflow on deeply cascaded circuits; (2) Rejects all feedback, prohibiting valid sequential logic (latches); (3) Does not yield topological evaluation levels directly."),
        ("Paper 3: Tarjan's Union-Find (1975)", "Robert E. Tarjan — Journal of the ACM (JACM), Vol. 22, No. 2, pp. 215–225",
         "Proved O(m * alpha(n)) amortized bound for Disjoint Sets using path compression and union by rank. Used for wire-net equivalence.",
         "Drawbacks: (1) Irreversible merges (supports union, but cannot split/disconnect wires); (2) Lacks signal directionality (cannot distinguish drivers from sinks); (3) Indirection overhead for small circuits.")
    ]

    for idx, (title_p, cit_p, cont_p, draw_p) in enumerate(papers):
        top = Inches(1.4 + idx * 1.8)
        create_card(s3, Inches(0.8), top, Inches(11.733), Inches(1.6))

        tb = s3.shapes.add_textbox(Inches(1.05), top + Inches(0.12), Inches(11.2), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title_p
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_DARK

        p = tf.add_paragraph()
        p.text = cit_p
        p.font.size = Pt(10)
        p.font.color.rgb = C_PURPLE
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = "Contribution: " + cont_p
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK

        p = tf.add_paragraph()
        p.text = "⚠️ " + draw_p
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_CORAL

    # =========================================================================
    # SLIDE 4: 3. Block Diagram & Algorithmic Novelty (4/9)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Block Diagram & Algorithmic Novelty / Contribution", 4)

    # 4 Architecture Blocks
    b_blocks = [
        ("MODULE 1: GRAPH BUILDER", "Adjacency List + Netlist", [
            "• Dual-direction storage: forward edges (adjList) + reverse edges (inputs)",
            "• O(1) amortized insertion",
            "• Union-Find wire net clustering"
        ], C_NAVY_DARK),
        ("MODULE 2: PRE-VALIDATION", "Tarjan's 3-Colour DFS", [
            "• Node states: WHITE, GRAY, BLACK",
            "• Back-edge caught on GRAY visit",
            "• Halts simulation and pinpoints offending gate IDs safely"
        ], C_CORAL),
        ("MODULE 3: SCHEDULER", "Kahn's BFS Topo-Sort", [
            "• In-degree tracking array",
            "• Zero in-degree queue seeds inputs",
            "• Guarantees data readiness at every gate before evaluation"
        ], C_PURPLE),
        ("MODULE 4: EXECUTION & UI", "Logic Engine + Web EDA", [
            "• 9 gate types boolean evaluation",
            "• Bitwise truth table generator (2^N)",
            "• Interactive web drag-and-drop UI with live glowing signals"
        ], C_EMERALD)
    ]

    for idx, (b_title, b_sub, b_items, b_color) in enumerate(b_blocks):
        left = Inches(0.8 + idx * 2.98)
        top = Inches(1.4)
        width = Inches(2.8)
        height = Inches(3.6)

        create_card(s4, left, top, width, height)

        strip = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.55))
        strip.fill.solid()
        strip.fill.fore_color.rgb = b_color
        strip.line.color.rgb = b_color

        tb = s4.shapes.add_textbox(left + Inches(0.1), top + Inches(0.06), width - Inches(0.2), Inches(0.45))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

        tb_c = s4.shapes.add_textbox(left + Inches(0.12), top + Inches(0.65), width - Inches(0.24), Inches(2.8))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        p = tf_c.paragraphs[0]
        p.text = b_sub
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = b_color
        p.space_after = Pt(8)

        for bi in b_items:
            p = tf_c.add_paragraph()
            p.text = bi
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(5)

    # Bottom Novelty Box
    create_card(s4, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.55), bg_color=RGBColor(232, 240, 254), border_color=C_NAVY_DARK)
    tb_nov = s4.shapes.add_textbox(Inches(1.05), Inches(5.35), Inches(11.2), Inches(1.25))
    tf_nov = tb_nov.text_frame
    tf_nov.word_wrap = True

    p = tf_nov.paragraphs[0]
    p.text = "⭐ Our Algorithmic Novelty & Technical Contribution:"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(4)

    p = tf_nov.add_paragraph()
    p.text = "1. Decoupled Pre-Validation Pipeline: Isolates cycle detection (DFS) from topological scheduling (Kahn's), preventing infinite execution loops common in basic simulators.\n2. Dual-Direction Graph Storage: Simultaneously preserves forward adjacency lists and reverse dependency vectors, allowing O(1) fan-in retrieval without matrix overhead.\n3. Combinatorial Bitwise Exhaustion: Uses direct bit shifts ((combo >> bit) & 1) to test all 2^N combinations in <1 ms, paired with 1:1 C++ and Web algorithm parity."
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 5: 4. Algorithms & Pseudocode — Validation & Scheduling (5/9)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Algorithms — DFS Cycle Detection & Kahn's Topo Sort", 5)

    # Left: DFS
    create_card(s5, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_dfs = s5.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(5.0))
    tf_dfs = tb_dfs.text_frame
    tf_dfs.word_wrap = True

    p = tf_dfs.paragraphs[0]
    p.text = "Algorithm 1: Tarjan's 3-Colour DFS (O(V+E))"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(8)

    code_dfs = """procedure HAS_CYCLE_DFS(u, color[], graph):
    color[u] ← GRAY // Active on recursion call stack
    for each v in graph.adjList[u] do:
        if color[v] == GRAY then
            return TRUE // Back-edge detected!
        if color[v] == WHITE then
            if HAS_CYCLE_DFS(v, color, graph) then
                return TRUE
    color[u] ← BLACK // Exploration complete
    return FALSE

procedure HAS_CYCLE(graph):
    color ← array of size V initialized to WHITE
    for i ← 0 to V - 1 do:
        if color[i] == WHITE then
            if HAS_CYCLE_DFS(i, color, graph) then
                return TRUE
    return FALSE"""

    p = tf_dfs.add_paragraph()
    p.text = code_dfs
    p.font.size = Pt(9.5)
    p.font.name = "Consolas"
    p.font.color.rgb = RGBColor(30, 40, 55)

    # Right: Kahn's Topo
    create_card(s5, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_kahn = s5.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.3), Inches(5.0))
    tf_kahn = tb_kahn.text_frame
    tf_kahn.word_wrap = True

    p = tf_kahn.paragraphs[0]
    p.text = "Algorithm 2: Kahn's BFS Topological Sort (O(V+E))"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(8)

    code_kahn = """procedure TOPOLOGICAL_SORT(graph):
    inDegree ← array of size V initialized to 0
    for u ← 0 to V - 1 do:
        for each v in graph.adjList[u] do:
            inDegree[v] ← inDegree[v] + 1

    queue Q ← empty FIFO queue
    for i ← 0 to V - 1 do:
        if inDegree[i] == 0 then
            Q.push(i) // Seed with Primary Inputs

    order ← empty list
    while Q is not empty do:
        curr ← Q.pop()
        order.append(curr)
        for each v in graph.adjList[curr] do:
            inDegree[v] ← inDegree[v] - 1
            if inDegree[v] == 0 then
                Q.push(v)
    return order"""

    p = tf_kahn.add_paragraph()
    p.text = code_kahn
    p.font.size = Pt(9.5)
    p.font.name = "Consolas"
    p.font.color.rgb = RGBColor(30, 40, 55)

    # =========================================================================
    # SLIDE 6: 4. Algorithms & Pseudocode — Logic Eval & Truth Table (6/9)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "4. Algorithms — Logic Evaluation & Truth Table Generator", 6)

    # Left: Evaluation
    create_card(s6, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_ev = s6.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(5.0))
    tf_ev = tb_ev.text_frame
    tf_ev.word_wrap = True

    p = tf_ev.paragraphs[0]
    p.text = "Algorithm 3: Gate Evaluation (O(fan-in))"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(8)

    code_ev = """procedure EVALUATE_GATE(gate, allGates):
    switch gate.type:
        case AND:
            res ← 1
            for inId in gate.inputGateIds do:
                res ← res & allGates[inId].val
            gate.outputValue ← res
        case OR:
            res ← 0
            for inId in gate.inputGateIds do:
                res ← res | allGates[inId].val
            gate.outputValue ← res
        case NOT:
            gate.outputValue ← !allGates[gate.inputGateIds[0]].val
        case XOR:
            res ← 0
            for inId in gate.inputGateIds do:
                res ← res ^ allGates[inId].val
            gate.outputValue ← res
        case NAND, NOR, XNOR:
            gate.outputValue ← !(AND / OR / XOR logic)
        case OUTPUT:
            gate.outputValue ← allGates[gate.inputGateIds[0]].val"""

    p = tf_ev.add_paragraph()
    p.text = code_ev
    p.font.size = Pt(8.5)
    p.font.name = "Consolas"
    p.font.color.rgb = RGBColor(30, 40, 55)

    # Right: Truth Table
    create_card(s6, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_tt = s6.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.3), Inches(5.0))
    tf_tt = tb_tt.text_frame
    tf_tt.word_wrap = True

    p = tf_tt.paragraphs[0]
    p.text = "Algorithm 4: Truth Table Generator (O(2^N * (V+E)))"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(8)

    code_tt = """procedure GENERATE_TRUTH_TABLE(circuit):
    inputs  ← all gates where type == INPUT
    outputs ← all gates where type == OUTPUT
    N ← inputs.size()
    totalRows ← 2^N

    for combo ← 0 to totalRows - 1 do:
        // 1. Bitwise extraction for Primary Inputs
        for i ← 0 to N - 1 do:
            bitPos ← N - 1 - i
            inputs[i].val ← (combo >> bitPos) & 1

        // 2. Full simulation in Topological Order
        SIMULATE(circuit, verbose = false)

        // 3. Record truth row
        printRow(inputs.values, outputs.values)

    // Guaranteed exhaustive functional validation"""

    p = tf_tt.add_paragraph()
    p.text = code_tt
    p.font.size = Pt(9.0)
    p.font.name = "Consolas"
    p.font.color.rgb = RGBColor(30, 40, 55)

    # =========================================================================
    # SLIDE 7: 5. Dataset — IEEE ISCAS '85 Standard Benchmarks (7/9)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "5. Dataset — IEEE ISCAS '85 Benchmark Suite (.bench)", 7)

    create_card(s7, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_d = s7.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.2), Inches(4.85))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "Dataset Specification & Download Links"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(10)

    d_items = [
        ("Industry Standard: ", "Published by IEEE International Symposium on Circuits and Systems (ISCAS); the worldwide benchmark for logic simulators and DAG algorithms."),
        ("Format (.bench): ", "Topological netlist specifying INPUT(...), OUTPUT(...), and gate assignments with explicit fan-ins."),
        ("Official Repositories: ", "• Univ. of Tennessee BVLS: https://pld.cs.utk.edu/bvls/iscas85/\n• Czech Technical Univ: https://ddd.fit.cvut.cz/prj/Benchmarks/\n• Trust-Hub Benchmark Suite: https://trust-hub.org/benchmarks"),
        ("Validation Method: ", "Evaluated simulator output against official published IEEE truth tables for accuracy verification.")
    ]
    for h, b in d_items:
        p = tf_d.add_paragraph()
        p.text = "• " + h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_CORAL
        p.space_after = Pt(2)
        p2 = tf_d.add_paragraph()
        p2.text = "  " + b
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_after = Pt(8)

    # Right: Benchmark Table
    create_card(s7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_dt = s7.shapes.add_textbox(Inches(7.05), Inches(1.65), Inches(5.2), Inches(4.85))
    tf_dt = tb_dt.text_frame
    tf_dt.word_wrap = True

    p = tf_dt.paragraphs[0]
    p.text = "Benchmark Suite Circuits & Our c17 Results"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(10)

    table_shape_b = s7.shapes.add_table(6, 4, Inches(7.0), Inches(2.2), Inches(5.3), Inches(2.7))
    tbl_b = table_shape_b.table
    b_headers = ["Circuit", "Inputs", "Outputs", "Gates & Function"]
    for c, h in enumerate(b_headers):
        cell = tbl_b.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE

    bench_rows = [
        ("c17", "5", "2", "6 NAND gates (Included in Demo!)"),
        ("c432", "36", "7", "160 gates (Interrupt Controller)"),
        ("c499", "41", "32", "202 gates (32-bit Error Correction)"),
        ("c880", "60", "26", "383 gates (8-bit ALU)"),
        ("c1355", "41", "32", "546 gates (32-bit SEC Circuit)")
    ]
    for r, rdata in enumerate(bench_rows):
        for c, val in enumerate(rdata):
            cell = tbl_b.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if (r % 2 == 0) else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            if r == 0:
                p.font.bold = True
                p.font.color.rgb = C_CORAL

    tb_res = s7.shapes.add_textbox(Inches(7.0), Inches(5.15), Inches(5.3), Inches(1.3))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True
    p = tf_res.paragraphs[0]
    p.text = "✓ c17 Live Benchmark Validation: Both our C++ executable (Option 14) and Web UI evaluate all 32/32 truth table rows in <1 ms, achieving 100% mathematical match with IEEE reference standards."
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    # =========================================================================
    # SLIDE 8: Dual Architecture Implementation & Web EDA (8/9)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "System Implementation — C++ Engine & Web EDA Canvas", 8)

    create_card(s8, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_cpp = s8.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.2), Inches(4.85))
    tf_cpp = tb_cpp.text_frame
    tf_cpp.word_wrap = True

    p = tf_cpp.paragraphs[0]
    p.text = "🖥️ High-Performance C++ Core Engine"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(10)

    cpp_features = [
        ("Static Zero-Dependency Binary: ", "simulator.exe (3.0 MB) compiled with -static; runs standalone on any Windows OS without missing DLLs."),
        ("Categorized CLI Menu: ", "Organized into Construction, Visualization, Analysis, and 4 Preset Demos."),
        ("Terminal ASCII Schematics: ", "Renders clear circuit schematics, pin maps, and wire paths directly in terminal text."),
        ("Diagnostic Gate Inspector: ", "Allows O(1) probing of any gate ID to inspect live signals, fan-in sources, and fan-out targets.")
    ]
    for h, b in cpp_features:
        p = tf_cpp.add_paragraph()
        p.text = "• " + h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY_DARK
        p.space_after = Pt(2)
        p2 = tf_cpp.add_paragraph()
        p2.text = "  " + b
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_after = Pt(8)

    create_card(s8, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.35))
    tb_web = s8.shapes.add_textbox(Inches(7.05), Inches(1.65), Inches(5.2), Inches(4.85))
    tf_web = tb_web.text_frame
    tf_web.word_wrap = True

    p = tf_web.paragraphs[0]
    p.text = "🌐 Interactive Drag-and-Drop Web Module (web/)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(10)

    web_features = [
        ("HTML5 Canvas EDA Environment: ", "Drag gates from left palette, connect cubic Bezier wires from output pins to input pins seamlessly."),
        ("Live Signal Flow & Glowing Wires: ", "Wires glow green when HIGH (1) and gray when LOW (0); output bulbs illuminate dynamically."),
        ("Interactive Input Switches: ", "Click any input switch on canvas to toggle 0/1 in real-time with instant signal propagation."),
        ("1:1 C++ Synchronization: ", "Click 'Export C++ Code' to generate exact Circuit.h code, or run python server.py for backend bridge.")
    ]
    for h, b in web_features:
        p = tf_web.add_paragraph()
        p.text = "• " + h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_CORAL
        p.space_after = Pt(2)
        p2 = tf_web.add_paragraph()
        p2.text = "  " + b
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_after = Pt(8)

    # =========================================================================
    # SLIDE 9: Complexity Analysis & Academic References (9/9)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Complexity Analysis, References & Review Conclusion", 9)

    # Complexity Table
    table_shape_c = s9.shapes.add_table(6, 4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(2.5))
    tbl_c = table_shape_c.table
    c_headers = ["Simulator Module / Operation", "Algorithm", "Time Complexity", "Space Complexity"]
    for c, h in enumerate(c_headers):
        cell = tbl_c.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_WHITE

    complexities = [
        ("Gate Insertion & Wire Routing", "Vector & Adjacency List Push", "O(1) amortized", "O(1)"),
        ("Cycle Pre-Validation", "Tarjan's 3-Colour DFS", "O(V + E)", "O(V) color vector"),
        ("Evaluation Scheduling", "Kahn's BFS Topological Sort", "O(V + E)", "O(V + E) in-degrees & queue"),
        ("Single Simulation Pass", "Topo Sort + Gate Evaluation", "O(V + E)", "O(V)"),
        ("Exhaustive Truth Table", "Bitwise Shifting (All 2^N Vectors)", "O(2^N * (V + E))", "O(V)")
    ]
    for r, rdata in enumerate(complexities):
        for c, val in enumerate(rdata):
            cell = tbl_c.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if (r % 2 == 0) else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            if c >= 2:
                p.font.name = "Consolas"
                p.font.bold = True
                p.font.color.rgb = C_CORAL if c == 2 else C_NAVY_DARK

    # References Box
    create_card(s9, Inches(0.8), Inches(4.2), Inches(11.733), Inches(2.6))
    tb_ref = s9.shapes.add_textbox(Inches(1.05), Inches(4.35), Inches(11.2), Inches(2.3))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True

    p = tf_ref.paragraphs[0]
    p.text = "📚 Formal Academic References & Review 1 Status:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(4)

    refs_list = [
        "1. Kahn, A. B. (1962). 'Topological sorting of large networks.' Communications of the ACM, 5(11), 558–562.",
        "2. Tarjan, R. E. (1972). 'Depth-First Search and Linear Graph Algorithms.' SIAM Journal on Computing, 1(2), 146–160.",
        "3. Tarjan, R. E. (1975). 'Efficiency of a Good but Not Linear Set Union Algorithm.' Journal of the ACM (JACM), 22(2), 215–225.",
        "4. Brglez, F., & Fujiwara, H. (1985). 'A neutral netlist of 10 combinational benchmark circuits.' IEEE ISCAS'85 Special Session.",
        "Status: First Review deliverables completed — working C++ CLI, interactive web GUI, ISCAS c17 benchmark, and slide deck."
    ]
    for rf in refs_list:
        p = tf_ref.add_paragraph()
        p.text = rf
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(3)

    prs.save(output_path)
    print(f"Concise 9-slide presentation saved to: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Projects\DigitalLogicSimulator"
    # Save both as concise version and main PPTX
    out_file1 = os.path.join(out_dir, "Digital_Logic_Simulator_First_Review_Short.pptx")
    out_file2 = os.path.join(out_dir, "Digital_Logic_Simulator_First_Review.pptx")
    create_short_deck(out_file1)
    create_short_deck(out_file2)
