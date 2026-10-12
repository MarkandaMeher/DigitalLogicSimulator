import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_pptx_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean academic palette (Human / University Review Style)
    C_NAVY = RGBColor(30, 58, 138)         # #1E3A8A - Primary Header
    C_SLATE_DARK = RGBColor(51, 65, 85)     # #334155 - Body Text
    C_MUTED = RGBColor(100, 116, 139)       # #64748B - Subtitles & Footers
    C_LINE = RGBColor(203, 213, 225)        # #CBD5E1 - Thin clean borders
    C_CARD_BG = RGBColor(248, 250, 252)     # #F8FAFC - Subtle box background
    C_CODE_BG = RGBColor(241, 245, 249)     # #F1F5F9 - Monospace code block background
    C_CODE_TEXT = RGBColor(15, 23, 42)      # #0F172A - Code text
    C_BLUE_ACCENT = RGBColor(37, 99, 235)   # #2563EB - Highlights & Titles
    C_WHITE = RGBColor(255, 255, 255)

    def add_academic_header(slide, section_tag, title_text, slide_num, total_slides=8):
        # Subtle top accent bar (thin, 2pt)
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.03))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = C_BLUE_ACCENT
        top_line.line.fill.background()

        # Header Text Box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_BLUE_ACCENT
        p_tag.font.name = "Arial"
        p_tag.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY
        p_title.font.name = "Arial"

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.3))
        tf_f = footer_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p_f = tf_f.paragraphs[0]
        p_f.text = f"First Review (Oct 12, 2026) | Digital Logic Circuit Simulator | Markanda Meher & Nikhil | Slide {slide_num} of {total_slides}"
        p_f.font.size = Pt(9.5)
        p_f.font.color.rgb = C_MUTED
        p_f.font.name = "Arial"

    def create_box(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_LINE):
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = bg_color
        box.line.color.rgb = border_color
        box.line.width = Pt(1)
        return box

    # =========================================================================
    # SLIDE 1: Title Slide (Clean, Academic, Minimalist)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Clean subtle background border
    frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame.fill.solid()
    frame.fill.fore_color.rgb = C_CARD_BG
    frame.line.color.rgb = C_LINE
    frame.line.width = Pt(1.5)

    # Top accent line
    t_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.08))
    t_line.fill.solid()
    t_line.fill.fore_color.rgb = C_NAVY
    t_line.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "COURSE PROJECT — FIRST REVIEW (OCTOBER 12, 2026)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.font.name = "Arial"
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "Digital Logic Circuit Simulator"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "A Graph-Theoretic Framework for Combinational Logic Validation & Simulation"
    p.font.size = Pt(17)
    p.font.color.rgb = C_SLATE_DARK
    p.font.name = "Arial"
    p.space_after = Pt(28)

    p = tf1.add_paragraph()
    p.text = "Presented by:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    p = tf1.add_paragraph()
    p.text = "• Markanda Meher  (Roll No. 206126020)\n• Nikhil  (Roll No. 206126021)"
    p.font.size = Pt(14)
    p.font.color.rgb = C_SLATE_DARK
    p.font.name = "Arial"
    p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "Department of Computer Science & Engineering | Advanced Data Structures & Algorithms"
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"

    # =========================================================================
    # SLIDE 2: 1. Introduction - Problem and Need
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_academic_header(s2, "Review Point 1", "1. Introduction — Problem Statement & Need for Solution", 2)

    # Left Column: The Problem in Physical Prototyping
    create_box(s2, Inches(0.8), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_prob = s2.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.15), Inches(4.7))
    tf_prob = tb_prob.text_frame
    tf_prob.word_wrap = True

    p = tf_prob.paragraphs[0]
    p.text = "The Problem: Physical Hardware Constraints"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(12)

    bullets_prob = [
        ("Breadboard Clutter & Tangled Wires: ", "Building multi-gate circuits physically requires manual jumper wires, prone to loose pins and high wiring clutter."),
        ("Tedious Fault Localization: ", "Isolating a faulty gate or incorrect connection requires manual probing with multimeters or oscilloscopes."),
        ("Risk of Hardware Damage: ", "Accidental short circuits, incorrect VCC/GND wiring, or reverse IC insertion can destroy physical 7400-series TTL chips."),
        ("Scalability Bottleneck: ", "Scaling to 20+ gates on physical breadboards becomes impractical for students and academic laboratories."),
        ("No Automated Design Rule Checks: ", "Physical boards cannot detect illegal feedback loops or race conditions before power is applied.")
    ]
    for title, desc in bullets_prob:
        p = tf_prob.add_paragraph()
        p.text = f"• {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_SLATE_DARK
        p.font.name = "Arial"
        p.space_after = Pt(2)
        
        # Add normal text description
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_SLATE_DARK
        p.space_after = Pt(8)

    # Right Column: The Need for Software Simulation
    create_box(s2, Inches(6.85), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_need = s2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.15), Inches(4.7))
    tf_need = tb_need.text_frame
    tf_need.word_wrap = True

    p = tf_need.paragraphs[0]
    p.text = "The Need: Graph-Theoretic Software Simulation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT
    p.font.name = "Arial"
    p.space_after = Pt(12)

    bullets_need = [
        ("Zero-Cost & Safe Experimentation: ", "Eliminates physical IC costs and equipment damage while enabling instant circuit restructuring."),
        ("Automated Cycle Detection: ", "Models circuits as directed graphs; executes linear-time cycle detection to catch illegal feedback loops instantly."),
        ("Topological Execution Ordering: ", "Guarantees mathematically that upstream gate signals settle before downstream gates evaluate, avoiding race conditions."),
        ("Exhaustive Truth Table Verification: ", "Automatically simulates all 2^N input combinations, proving circuit equivalence against theoretical Boolean algebra."),
        ("Pedagogical Transparency: ", "Shows the direct application of fundamental graph algorithms (DFS, Kahn's BFS, Disjoint Sets) in computer engineering.")
    ]
    for title, desc in bullets_need:
        p = tf_need.add_paragraph()
        p.text = f"• {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_SLATE_DARK
        p.font.name = "Arial"
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_SLATE_DARK
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: 2. Literature Survey - 3 Papers & Drawbacks
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_academic_header(s3, "Review Point 2", "2. Literature Survey — Analysis of 3 Papers & Their Drawbacks", 3)

    papers = [
        {
            "paper": "Paper 1: A. B. Kahn (1962)",
            "title": "Topological Sorting of Large Networks",
            "venue": "Communications of the ACM, Vol. 5, No. 11, pp. 558–562",
            "contents": "Introduced in-degree based queue processing (BFS style) to establish a linear processing sequence in Directed Acyclic Graphs with O(V + E) runtime complexity.",
            "drawbacks": [
                "Does not identify exact cycle location: If in-degrees never reach zero, it halts without reporting the offending cycle path or back-edge.",
                "Arbitrary tie-breaking: Does not optimize for circuit levelization (parallel gate stages), picking arbitrary zero-indegree nodes."
            ]
        },
        {
            "paper": "Paper 2: R. E. Tarjan (1972)",
            "title": "Depth-First Search and Linear Graph Algorithms",
            "venue": "SIAM Journal on Computing, Vol. 1, No. 2, pp. 146–160",
            "contents": "Formulated 3-state depth-first search (White/Gray/Black node coloration) and strongly connected components (SCC) running in linear O(V + E) time.",
            "drawbacks": [
                "Recursion stack vulnerability: Standard recursive implementations risk call-stack overflow on deep logic paths in large netlists.",
                "Lacks evaluation schedule: Identifying SCCs or back-edges proves cycle presence, but does not provide an execution order for logic simulation."
            ]
        },
        {
            "paper": "Paper 3: R. E. Tarjan (1975)",
            "title": "Efficiency of a Good But Not Linear Set Union Algorithm",
            "venue": "Journal of the ACM, Vol. 22, No. 2, pp. 215–225",
            "contents": "Analyzed Disjoint-Set Union (DSU) with union-by-rank and path compression, proving near-linear O(alpha(N)) amortized operational bounds.",
            "drawbacks": [
                "Symmetric / Undirected only: Merges connected components bidirectionally, failing to enforce directed signal propagation (driver-to-load).",
                "Irreversible union operations: Standard DSU cannot easily split connected wire nets when a user removes a single wire connection."
            ]
        }
    ]

    card_y = 1.6
    card_h = 1.6
    gap = 0.15

    for idx, p_info in enumerate(papers):
        y_pos = Inches(card_y + idx * (card_h + gap))
        create_box(s3, Inches(0.8), y_pos, Inches(11.733), Inches(card_h))
        
        tb = s3.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.1), Inches(11.333), Inches(card_h - 0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{p_info['paper']}: \"{p_info['title']}\" — {p_info['venue']}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.font.name = "Arial"
        p.space_after = Pt(3)

        p = tf.add_paragraph()
        p.text = "• Analysis / Contribution: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_SLATE_DARK
        p.font.name = "Arial"
        run = p.add_run()
        run.text = p_info["contents"]
        run.font.bold = False
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = "• Specific Drawbacks: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(185, 28, 28) # Red accent for drawbacks
        p.font.name = "Arial"
        run = p.add_run()
        run.text = f"(1) {p_info['drawbacks'][0]} (2) {p_info['drawbacks'][1]}"
        run.font.bold = False
        run.font.color.rgb = C_SLATE_DARK

    # =========================================================================
    # SLIDE 4: 3. Block Diagram & Algorithmic Novelty
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_academic_header(s4, "Review Point 3", "3. Block Diagram & Algorithmic Novelty", 4)

    # Left: Block Diagram Flow (Horizontal / Vertical Modular Layout)
    create_box(s4, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.1))
    tb_bd = s4.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(6.4), Inches(4.8))
    tf_bd = tb_bd.text_frame
    tf_bd.word_wrap = True

    p = tf_bd.paragraphs[0]
    p.text = "System Block Diagram: 4-Stage Simulation Architecture"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(10)

    modules = [
        ("Module 1: Circuit Graph Model", "Directed Graph G = (V, E) via Adjacency List. Gates = Vertices, Wires = Directed Edges. In-degree and predecessor mapping."),
        ("Module 2: Cycle Detection Engine", "Tarjan's 3-Color DFS (White/Gray/Black). Re-encountering a Gray node traps illegal back-edges and halts invalid feedback loops."),
        ("Module 3: Evaluation Order Scheduler", "Kahn's Topological Sort (In-Degree Queue BFS). Produces strict linear execution schedule ensuring upstream dependencies settle first."),
        ("Module 4: Logic Execution & Verification", "Boolean Gate Switch Engine + Exhaustive 2^N Truth Table Generator. Computes outputs and verifies circuit logic.")
    ]

    for m_title, m_desc in modules:
        p = tf_bd.add_paragraph()
        p.text = f"▼  {m_title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_BLUE_ACCENT
        p.font.name = "Arial"
        p.space_after = Pt(2)

        p = tf_bd.add_paragraph()
        p.text = m_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_SLATE_DARK
        p.font.name = "Arial"
        p.space_after = Pt(6)

    # Right: Algorithmic Novelty & Contribution
    create_box(s4, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.1))
    tb_nov = s4.shapes.add_textbox(Inches(8.0), Inches(1.75), Inches(4.333), Inches(4.8))
    tf_nov = tb_nov.text_frame
    tf_nov.word_wrap = True

    p = tf_nov.paragraphs[0]
    p.text = "Algorithmic Novelty & Contribution"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(12)

    novelty_points = [
        ("Dual-Phase Graph Validation: ", "Decouples cycle identification from evaluation scheduling. Uses 3-color DFS specifically to isolate and report offending feedback edges, then uses Kahn's algorithm for deterministic levelized scheduling."),
        ("Strict Dependency Invariance: ", "Guarantees zero race conditions. In combinational circuits, every gate evaluates strictly after all its upstream driver inputs are stabilized in O(V + E) time."),
        ("Fast O(1) Hash Map Gate Indexing: ", "Provides instantaneous retrieval of gates, netlists, and pin states by name, eliminating O(V) scan overheads during multi-gate propagation."),
        ("Automated Exhaustive Verification: ", "Bitwise simulation engine generates full truth tables across all 2^N input permutations, catching logic bugs without physical test vectors.")
    ]

    for n_title, n_desc in novelty_points:
        p = tf_nov.add_paragraph()
        p.text = f"• {n_title}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_SLATE_DARK
        p.font.name = "Arial"
        
        run = p.add_run()
        run.text = n_desc
        run.font.bold = False
        run.font.color.rgb = C_SLATE_DARK
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 5: 4. Algorithms / Pseudo Code (Modules 1 & 2)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_academic_header(s5, "Review Point 4 (Part 1)", "4. Algorithms / Pseudocode — Graph Representation & Cycle Detection", 5)

    # Left: Module 1 Pseudocode (Graph Construction)
    create_box(s5, Inches(0.8), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_m1 = s5.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.25), Inches(4.8))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True

    p = tf_m1.paragraphs[0]
    p.text = "Module 1: Graph Model & Netlist Builder"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    p = tf_m1.add_paragraph()
    p.text = "Data Structure: Directed Graph G = (V, E) with Adjacency List"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"
    p.space_after = Pt(8)

    code_m1 = """Algorithm BuildCircuitGraph(Gates V, Wires E):
1:  adjList  = HashMap<GateID, List<GateID>>()
2:  inDegree = HashMap<GateID, Integer>()
3:  For each gate g in V:
4:      adjList[g.id] = empty_list()
5:      inDegree[g.id] = 0
6:  For each wire (u, v) in E:
7:      // u is driver gate, v is load gate
8:      adjList[u].append(v)
9:      inDegree[v] = inDegree[v] + 1
10: Return (adjList, inDegree)

Time Complexity:  O(V + E)
Space Complexity: O(V + E)"""

    p = tf_m1.add_paragraph()
    p.text = code_m1
    p.font.size = Pt(10)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # Right: Module 2 Pseudocode (Cycle Detection)
    create_box(s5, Inches(6.85), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_m2 = s5.shapes.add_textbox(Inches(7.05), Inches(1.75), Inches(5.25), Inches(4.8))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True

    p = tf_m2.paragraphs[0]
    p.text = "Module 2: Cycle Detection (Tarjan's 3-Color DFS)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    p = tf_m2.add_paragraph()
    p.text = "Detects illegal feedback loops: WHITE=Unvisited, GRAY=Active, BLACK=Done"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"
    p.space_after = Pt(8)

    code_m2 = """Algorithm HasCycleDFS(u, color, adjList):
1:  color[u] = GRAY  // Currently in recursion stack
2:  For each neighbor v in adjList[u]:
3:      If color[v] == GRAY:
4:          RecordCycleBackEdge(u, v)
5:          Return TRUE  // Cycle detected!
6:      If color[v] == WHITE:
7:          If HasCycleDFS(v, color, adjList) == TRUE:
8:              Return TRUE
9:  color[u] = BLACK // Subtree verified cycle-free
10: Return FALSE

Time Complexity:  O(V + E)
Space Complexity: O(V) recursion stack"""

    p = tf_m2.add_paragraph()
    p.text = code_m2
    p.font.size = Pt(10)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # =========================================================================
    # SLIDE 6: 4. Algorithms / Pseudo Code (Modules 3 & 4)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_academic_header(s6, "Review Point 4 (Part 2)", "4. Algorithms / Pseudocode — Scheduling & Logic Simulation", 6)

    # Left: Module 3 Pseudocode (Kahn's Algorithm)
    create_box(s6, Inches(0.8), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_m3 = s6.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.25), Inches(4.8))
    tf_m3 = tb_m3.text_frame
    tf_m3.word_wrap = True

    p = tf_m3.paragraphs[0]
    p.text = "Module 3: Evaluation Scheduler (Kahn's Topo Sort)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    p = tf_m3.add_paragraph()
    p.text = "Determines strictly valid gate evaluation order via in-degree BFS"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"
    p.space_after = Pt(8)

    code_m3 = """Algorithm KahnTopologicalSort(V, inDegree, adjList):
1:  Q = EmptyQueue()
2:  For each gate g in V:
3:      If inDegree[g] == 0: Q.push(g)
4:  evalOrder = []
5:  While Q is not empty:
6:      u = Q.pop()
7:      evalOrder.append(u)
8:      For each v in adjList[u]:
9:          inDegree[v] = inDegree[v] - 1
10:         If inDegree[v] == 0: Q.push(v)
11: Return evalOrder

Time Complexity:  O(V + E)
Space Complexity: O(V)"""

    p = tf_m3.add_paragraph()
    p.text = code_m3
    p.font.size = Pt(10)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # Right: Module 4 Pseudocode (Gate Logic & Simulation)
    create_box(s6, Inches(6.85), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_m4 = s6.shapes.add_textbox(Inches(7.05), Inches(1.75), Inches(5.25), Inches(4.8))
    tf_m4 = tb_m4.text_frame
    tf_m4.word_wrap = True

    p = tf_m4.paragraphs[0]
    p.text = "Module 4: Logic Execution & Truth Table Engine"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    p = tf_m4.add_paragraph()
    p.text = "Propagates boolean states through ordered gates and verifies outputs"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"
    p.space_after = Pt(8)

    code_m4 = """Algorithm SimulateCircuit(evalOrder, inputVector):
1:  values = HashMap<GateID, Boolean>()
2:  For each g in evalOrder:
3:      If g.type == INPUT:
4:          values[g] = inputVector[g.id]
5:      Else:
6:          inVals = [values[p] for p in g.predecessors]
7:          values[g] = EvaluateGate(g.type, inVals)
8:  Return values

Algorithm GenerateTruthTable(N_inputs, evalOrder):
1:  For row = 0 to (2^N - 1):
2:      inputVector = DecodeBits(row, N_inputs)
3:      outputRow = SimulateCircuit(evalOrder, inputVector)
4:      PrintTruthTableRow(inputVector, outputRow)"""

    p = tf_m4.add_paragraph()
    p.text = code_m4
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # =========================================================================
    # SLIDE 7: 5. Dataset - IEEE ISCAS '85 Suite
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_academic_header(s7, "Review Point 5", "5. Dataset — IEEE ISCAS '85 Benchmark Circuit Suite", 7)

    # Left: Links & Explanation of Contents
    create_box(s7, Inches(0.8), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_ds = s7.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(5.15), Inches(4.8))
    tf_ds = tb_ds.text_frame
    tf_ds.word_wrap = True

    p = tf_ds.paragraphs[0]
    p.text = "Benchmark Suite & Repository Links"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(10)

    ds_info = [
        ("Dataset Name: ", "IEEE ISCAS '85 Benchmark Suite (International Symposium on Circuits and Systems)."),
        ("Industry Standard: ", "The universally accepted benchmark suite in Electronic Design Automation (EDA) and academic CAD research for combinational circuit validation."),
        ("Repository Link 1 (Primary): ", "University of Tennessee EECS CAD Lab:\nhttps://web.eecs.utk.edu/~troy/benchmark/"),
        ("Repository Link 2 (Mirror): ", "Czech Technical University (FEE CTU Benchmarks):\nhttps://ddd.fit.cvut.cz/prj/Benchmarks/"),
        ("Netlist Format (.bench): ", "Human-readable ASCII defining Primary Inputs (INPUT), Primary Outputs (OUTPUT), and gate connection equations (e.g., 10 = NAND(1, 3)).")
    ]

    for title, desc in ds_info:
        p = tf_ds.add_paragraph()
        p.text = f"• {title}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_SLATE_DARK
        p.font.name = "Arial"
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_SLATE_DARK
        p.space_after = Pt(8)

    # Right: Benchmark Circuits Used & Purpose in Project
    create_box(s7, Inches(6.85), Inches(1.6), Inches(5.65), Inches(5.1))
    tb_role = s7.shapes.add_textbox(Inches(7.1), Inches(1.75), Inches(5.15), Inches(4.8))
    tf_role = tb_role.text_frame
    tf_role.word_wrap = True

    p = tf_role.paragraphs[0]
    p.text = "Benchmark Circuits & Project Role"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(10)

    bench_circuits = [
        ("c17 (6 Gates, 5 Inputs, 2 Outputs): ", "Smallest ISCAS netlist; used for fundamental algorithmic sanity checks and truth table validation across all 32 combinations."),
        ("c432 (160 Gates, 36 Inputs, 7 Outputs): ", "27-channel interrupt controller; tests topological scheduling performance on medium-scale fanout networks."),
        ("c499 (202 Gates, 41 Inputs, 32 Outputs): ", "32-bit single-error-correcting circuit (SEC-DED); verifies deep logic paths."),
        ("c880 (383 Gates, 60 Inputs, 26 Outputs): ", "8-bit Arithmetic Logic Unit (ALU); evaluates asymptotic time complexity and memory scaling on 380+ nodes.")
    ]

    for title, desc in bench_circuits:
        p = tf_role.add_paragraph()
        p.text = f"• {title}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_BLUE_ACCENT
        p.font.name = "Arial"
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_SLATE_DARK
        p.space_after = Pt(6)

    p = tf_role.add_paragraph()
    p.text = "Purpose in Project: Verifies cycle detection, proves logic correctness against reference truth tables, and demonstrates linear O(V + E) scalability."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 8: Summary / Questions
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_academic_header(s8, "Conclusion", "Summary of First Review Deliverables & Review Alignment", 8)

    create_box(s8, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
    tb_sum = s8.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.133), Inches(4.7))
    tf_sum = tb_sum.text_frame
    tf_sum.word_wrap = True

    p = tf_sum.paragraphs[0]
    p.text = "Review Alignment Matrix"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(12)

    matrix_rows = [
        ("1. Problem Statement & Need: ", "Demonstrated the physical constraints of breadboard circuits and established the need for a software DAG simulator."),
        ("2. Literature Survey: ", "Analyzed 3 landmark papers (Kahn 1962, Tarjan 1972 DFS, Tarjan 1975 DSU) and clearly identified their algorithmic drawbacks."),
        ("3. Block Diagram & Novelty: ", "Presented a 4-module architecture featuring dual-phase graph validation (DFS cycle isolation + Kahn's levelized scheduling)."),
        ("4. Algorithms & Pseudocode: ", "Provided formal pseudocode and asymptotic analysis for all 4 modules (Graph Builder, 3-Color DFS, Kahn's BFS, Logic Simulation)."),
        ("5. Dataset & Benchmark: ", "Documented the official IEEE ISCAS '85 suite with university download links and verified c17 truth table correctness.")
    ]

    for title, desc in matrix_rows:
        p = tf_sum.add_paragraph()
        p.text = f"✔ {title}"
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_BLUE_ACCENT
        p.font.name = "Arial"
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_SLATE_DARK
        p.space_after = Pt(10)

    p = tf_sum.add_paragraph()
    p.text = "Thank You. Open for Questions from the Review Committee."
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    # Save presentation
    prs.save(output_pptx_path)
    print(f"Presentation saved successfully to: {output_pptx_path}")

if __name__ == "__main__":
    output_path = r"c:\Projects\DigitalLogicSimulator\Digital_Logic_Simulator_First_Review.pptx"
    build_presentation(output_path)
