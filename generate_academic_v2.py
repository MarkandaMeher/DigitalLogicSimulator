import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_pptx_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Refined Academic Color Palette
    C_NAVY = RGBColor(20, 35, 60)          # #14233C - Deep Oxford Navy (Titles)
    C_SLATE = RGBColor(50, 60, 75)         # #323C4B - Slate Charcoal (Body Text)
    C_BLUE = RGBColor(28, 90, 160)         # #1C5AA0 - Academic Accent Blue
    C_CRIMSON = RGBColor(165, 30, 40)      # #A51E28 - Drawbacks & Limitations
    C_MUTED = RGBColor(105, 115, 130)      # #697382 - Metadata & Footers
    C_LINE = RGBColor(215, 222, 230)       # #D7DEE6 - Subtle Dividers
    C_WHITE = RGBColor(255, 255, 255)
    C_ALGO_BG = RGBColor(250, 252, 254)    # Subtle off-white for algorithm canvas
    C_CODE_TEXT = RGBColor(15, 23, 42)

    def add_slide_header(slide, section_tag, title_text, slide_num, total_slides=12):
        # Top subtle rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.45), Inches(11.733), Inches(0.025))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_BLUE
        rule.line.fill.background()

        # Header Text Box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.85))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(10.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_BLUE
        p_tag.font.name = "Arial"
        p_tag.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY
        p_title.font.name = "Arial"

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf_f = footer_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p_f = tf_f.paragraphs[0]
        p_f.text = f"First Review (Oct 12, 2026) | Digital Logic Circuit Simulator | Markanda Meher & Nikhil | Slide {slide_num} of {total_slides}"
        p_f.font.size = Pt(9.5)
        p_f.font.color.rgb = C_MUTED
        p_f.font.name = "Arial"

    # =========================================================================
    # SLIDE 1: Title Slide (Refined Academic Presentation)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Clean framing line
    frame_rule = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(0.04))
    frame_rule.fill.solid()
    frame_rule.fill.fore_color.rgb = C_BLUE
    frame_rule.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(10.933), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(6)

    p = tf1.add_paragraph()
    p.text = "Advanced Data Structures & Algorithms — Course Project"
    p.font.size = Pt(14)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"
    p.space_after = Pt(22)

    p = tf1.add_paragraph()
    p.text = "Digital Logic Circuit Simulator"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "A Graph-Theoretic Framework for Combinational Logic Validation & Simulation"
    p.font.size = Pt(18)
    p.font.color.rgb = C_SLATE
    p.font.name = "Arial"
    p.space_after = Pt(36)

    p = tf1.add_paragraph()
    p.text = "Presented by:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    p = tf1.add_paragraph()
    p.text = "Markanda Meher (Roll No. 206126020)   |   Nikhil (Roll No. 206126021)"
    p.font.size = Pt(15)
    p.font.color.rgb = C_SLATE
    p.font.name = "Arial"
    p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "First Review — October 12, 2026"
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"

    # =========================================================================
    # SLIDE 2: 1. Introduction — Physical Prototyping Bottlenecks
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "1. Introduction & Problem Definition", "Physical Digital Circuit Prototyping Bottlenecks", 2, 12)

    # Left Column: Hardware Bottlenecks
    tb_s2_l = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tf_s2_l = tb_s2_l.text_frame
    tf_s2_l.word_wrap = True

    p = tf_s2_l.paragraphs[0]
    p.text = "Hardware Prototyping Constraints"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(14)

    pts_s2_l = [
        ("Discrete Breadboard Congestion: ", "Constructing multi-gate combinational designs requires dozens of physical jumper wires. Loose pin contacts, contact bounce, and wiring clutter frequently obscure connectivity."),
        ("Absence of Automated Verification: ", "Physical breadboards lack any design-rule checking mechanism. Illegal configurations—such as unwanted circular feedback loops or shorted gate outputs—are undetectable prior to powering the circuit."),
        ("Component Damage & Resource Waste: ", "Accidental reverse polarity, inverted IC pin insertion, or shorted VCC/GND traces permanently destroy 7400-series TTL/CMOS integrated circuits, incurring recurring laboratory replacement costs."),
        ("Tedious Manual Fault Localization: ", "Isolating a single faulty connection or burned gate requires slow, manual node-by-node probing with multimeters or oscilloscopes.")
    ]
    for bold_text, normal_text in pts_s2_l:
        p = tf_s2_l.add_paragraph()
        p.text = f"• {bold_text}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(10)

    # Right Column: Pedagogical & Scalability Limitations
    tb_s2_r = s2.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.1))
    tf_s2_r = tb_s2_r.text_frame
    tf_s2_r.word_wrap = True

    p = tf_s2_r.paragraphs[0]
    p.text = "Academic & Scalability Impact"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(14)

    pts_s2_r = [
        ("High Cognitive Debugging Overhead: ", "Students and engineers often spend over 70% of experimental laboratory sessions troubleshooting physical wire loose ends rather than studying digital logic and computer architecture fundamentals."),
        ("Strict Scalability Ceiling: ", "Scaling beyond 15–20 logic gates (e.g., 4-bit Arithmetic Logic Units, multiplexer trees, or multi-bit adders) becomes physically impractical on educational breadboard layouts."),
        ("Need for Pre-Silicon Modeling: ", "Modern VLSI engineering mandates software verification before hardware fabrication. An educational simulator bridges this gap by demonstrating how algorithmic models replace costly physical trial-and-error.")
    ]
    for bold_text, normal_text in pts_s2_r:
        p = tf_s2_r.add_paragraph()
        p.text = f"• {bold_text}"
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: 1. Introduction — The Software Simulation Paradigm
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "1. Introduction & Problem Definition", "The Graph-Theoretic Software Simulation Paradigm", 3, 12)

    tb_s3_l = s3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tf_s3_l = tb_s3_l.text_frame
    tf_s3_l.word_wrap = True

    p = tf_s3_l.paragraphs[0]
    p.text = "Mathematical Graph Abstraction"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(14)

    pts_s3_l = [
        ("Directed Graph Formalism: ", "A digital combinational circuit is mathematically modeled as a Directed Acyclic Graph G = (V, E), where logic gates are vertices and interconnecting wires are directed edges."),
        ("Strict Signal Causality: ", "Directed edges enforce physical signal propagation—signals flow strictly from driver output pins into load input pins with zero ambiguity."),
        ("Decoupling Geometry from Logic: ", "Abstracts away physical wire resistance, capacitance, and mechanical wear, allowing focus purely on functional correctness and topological structure.")
    ]
    for bold_text, normal_text in pts_s3_l:
        p = tf_s3_l.add_paragraph()
        p.text = f"• {bold_text}"
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(12)

    tb_s3_r = s3.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.1))
    tf_s3_r = tb_s3_r.text_frame
    tf_s3_r.word_wrap = True

    p = tf_s3_r.paragraphs[0]
    p.text = "Simulation Capabilities & Objectives"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(14)

    pts_s3_r = [
        ("Automated Cycle Trapping: ", "Traverses the graph in linear time O(V + E) to detect feedback loops before simulation begins, preventing infinite oscillation in combinational circuits."),
        ("Topological Execution Ordering: ", "Computes a valid evaluation schedule, guaranteeing every gate computes only after all its input dependencies have settled, eliminating race conditions."),
        ("Exhaustive Truth Table Generation: ", "Simulates all 2^N input combinations automatically, verifying logical equivalence against theoretical Boolean algebra in milliseconds."),
        ("Safe, Zero-Cost Experimentation: ", "Enables students to freely modify netlists, probe individual gate pins, and validate complex architectures with zero hardware costs.")
    ]
    for bold_text, normal_text in pts_s3_r:
        p = tf_s3_r.add_paragraph()
        p.text = f"• {bold_text}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 4: 2. Literature Survey — Paper 1: Kahn (1962)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "2. Literature Survey (Paper 1 of 3)", "In-Degree Topological Sorting (Kahn, 1962)", 4, 12)

    tb_s4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True

    p = tf_s4.paragraphs[0]
    p.text = "Citation: A. B. Kahn, \"Topological Sorting of Large Networks\", Communications of the ACM, Vol. 5, No. 11, pp. 558–562, Nov. 1962."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(14)

    p = tf_s4.add_paragraph()
    p.text = "Analysis of Algorithmic Contents & Contributions:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    kahn_contribs = [
        "Introduced the in-degree reduction queue paradigm for establishing linear execution schedules in Directed Acyclic Graphs (DAGs).",
        "Operates in optimal linear time O(V + E) by tracking in-degrees and enqueuing vertices whose dependencies reach zero.",
        "Forms the foundational algorithmic basis for dependency resolution in compilers, task schedulers, and EDA netlist simulation."
    ]
    for c in kahn_contribs:
        p = tf_s4.add_paragraph()
        p.text = f"•  {c}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        p.space_after = Pt(4)

    p = tf_s4.add_paragraph()
    p.text = "Critical Drawbacks & Limitations for Circuit Simulation:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    p.font.name = "Arial"
    p.space_after = Pt(6)

    kahn_drawbacks = [
        ("Silent Failure on Cycles (No Localization): ", "If the netlist contains a feedback loop, Kahn's algorithm halts prematurely when the queue becomes empty with unprocessed gates remaining. Crucially, it cannot pinpoint which specific back-edge or gates formed the cycle."),
        ("Arbitrary Tie-Breaking: ", "When multiple gates reach in-degree zero simultaneously, Kahn's algorithm dequeues in arbitrary queue order, failing to organize gates into levelized parallel stages."),
        ("Static In-Degree Assumption: ", "Assumes graph topology is completely static; modifying or deleting a wire requires full re-computation of all vertex in-degrees from scratch.")
    ]
    for bold_text, normal_text in kahn_drawbacks:
        p = tf_s4.add_paragraph()
        p.text = f"•  {bold_text}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 5: 2. Literature Survey — Paper 2: Tarjan (1972)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "2. Literature Survey (Paper 2 of 3)", "DFS & Linear Graph Connectivity (Tarjan, 1972)", 5, 12)

    tb_s5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True

    p = tf_s5.paragraphs[0]
    p.text = "Citation: R. E. Tarjan, \"Depth-First Search and Linear Graph Algorithms\", SIAM Journal on Computing, Vol. 1, No. 2, pp. 146–160, June 1972."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(14)

    p = tf_s5.add_paragraph()
    p.text = "Analysis of Algorithmic Contents & Contributions:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    tarj1_contribs = [
        "Formalized Depth-First Search using 3-state node classification (White = unvisited, Gray = active in call stack, Black = fully explored).",
        "Established linear-time O(V + E) algorithms for detecting strongly connected components (SCC), articulation points, and cycle back-edges.",
        "Introduced discovery/finishing timestamps and low-link tracking for deep structural graph decomposition."
    ]
    for c in tarj1_contribs:
        p = tf_s5.add_paragraph()
        p.text = f"•  {c}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        p.space_after = Pt(4)

    p = tf_s5.add_paragraph()
    p.text = "Critical Drawbacks & Limitations for Circuit Simulation:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    p.font.name = "Arial"
    p.space_after = Pt(6)

    tarj1_drawbacks = [
        ("Recursion Call-Stack Overhead: ", "Standard recursive implementations allocate O(V) stack frames. In deep combinational ripple circuits or large-scale netlists, this risks system stack overflow."),
        ("No Forward Evaluation Schedule: ", "While DFS back-edges isolate cycles perfectly, the resulting reverse post-order traversal is inherently backward-directed and does not yield levelized forward simulation stages."),
        ("Single-Pin Node Simplification: ", "Classical graph DFS treats each vertex as an atomic scalar entity, failing to handle multiple input pins with distinct logical positions (e.g., MUX select vs data pins).")
    ]
    for bold_text, normal_text in tarj1_drawbacks:
        p = tf_s5.add_paragraph()
        p.text = f"•  {bold_text}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 6: 2. Literature Survey — Paper 3: Tarjan (1975)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "2. Literature Survey (Paper 3 of 3)", "Disjoint-Set Union & Net Equivalence (Tarjan, 1975)", 6, 12)

    tb_s6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.2))
    tf_s6 = tb_s6.text_frame
    tf_s6.word_wrap = True

    p = tf_s6.paragraphs[0]
    p.text = "Citation: R. E. Tarjan, \"Efficiency of a Good But Not Linear Set Union Algorithm\", Journal of the ACM, Vol. 22, No. 2, pp. 215–225, April 1975."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(14)

    p = tf_s6.add_paragraph()
    p.text = "Analysis of Algorithmic Contents & Contributions:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    tarj2_contribs = [
        "Analyzed the Disjoint-Set Union (DSU) data structure combining union-by-rank and path compression heuristics.",
        "Proved the theoretical amortized operational complexity of O(m · alpha(m, n)), where alpha is the inverse Ackermann function (effectively <= 4 for all practical values).",
        "Widely utilized in EDA netlist parsing to group connected electrical pins into unified equipotential wire nets."
    ]
    for c in tarj2_contribs:
        p = tf_s6.add_paragraph()
        p.text = f"•  {c}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        p.space_after = Pt(4)

    p = tf_s6.add_paragraph()
    p.text = "Critical Drawbacks & Limitations for Circuit Simulation:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    p.font.name = "Arial"
    p.space_after = Pt(6)

    tarj2_drawbacks = [
        ("Symmetric / Undirected Equivalence Only: ", "DSU partitions vertices into undirected equivalence classes. It cannot enforce directional signal propagation (it cannot distinguish a driving gate output pin from driven load gate inputs)."),
        ("Irreversible Union Operations: ", "Standard DSU does not support set splitting. If a user deletes a wire connection between two gates, the entire disjoint set forest must be rebuilt from scratch in O(E) time."),
        ("No Execution Ordering: ", "DSU tracks connectivity only; it provides zero capability for scheduling Boolean gate evaluations.")
    ]
    for bold_text, normal_text in tarj2_drawbacks:
        p = tf_s6.add_paragraph()
        p.text = f"•  {bold_text}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 7: 2. Literature Survey — Comparative Summary Table
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "2. Literature Survey", "Comparative Evaluation: Surveyed Algorithms vs. Proposed Simulator", 7, 12)

    # Create Native PowerPoint Table for clean human presentation
    table_shape = s7.shapes.add_table(6, 5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(4.8))
    table = table_shape.table

    # Column Widths
    table.columns[0].width = Inches(2.333)
    table.columns[1].width = Inches(2.35)
    table.columns[2].width = Inches(2.35)
    table.columns[3].width = Inches(2.35)
    table.columns[4].width = Inches(2.35)

    headers = ["Evaluation Metric", "Kahn (1962)", "Tarjan DFS (1972)", "Tarjan DSU (1975)", "Our Simulator"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY if col_idx < 4 else C_BLUE
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

    row_data = [
        ("Primary Algorithmic Purpose", "Topological Ordering via In-Degree Queue", "Graph Traversal & SCC Decomposition", "Disjoint-Set Net Connectivity", "End-to-End Logic Simulation & Verification"),
        ("Time Complexity", "O(V + E) linear", "O(V + E) linear", "O(m · α(n)) near-linear", "O(V + E) linear"),
        ("Cycle Localization", "No (halts silently when queue empties)", "Yes (detects back-edges)", "N/A (undirected sets)", "Yes (isolates & logs exact cycle path)"),
        ("Execution Scheduling", "Yes (valid linear topological order)", "Requires reverse post-order traversal", "No (tracks connectivity only)", "Yes (guaranteed race-free evaluation)"),
        ("Directional Flow & Logic Eval", "Directional only (no logic evaluation)", "Directional only (no logic evaluation)", "Undirected only (no signal direction)", "Directional + Multi-gate Boolean truth tables")
    ]

    for row_idx, r_vals in enumerate(row_data, start=1):
        for col_idx, val in enumerate(r_vals):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(245, 248, 252) if col_idx == 4 else (C_WHITE if row_idx % 2 == 1 else RGBColor(248, 250, 252))
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.bold = (col_idx == 0 or col_idx == 4)
            p.font.color.rgb = C_NAVY if col_idx == 4 else C_SLATE
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 8: 3. Block Diagram — System Architecture & Dataflow
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "3. System Architecture", "4-Stage Simulation Architecture & Dataflow Pipeline", 8, 12)

    # Process Flow Shapes with Arrows (Real visual block diagram)
    stages = [
        ("Stage 1: Netlist & Graph Model", "Builds Directed Graph G=(V,E)\nAdjacency List & In-Degrees\nO(1) Hash Map Gate Indexing", Inches(0.8)),
        ("Stage 2: Cycle Detection Engine", "Tarjan's 3-Color DFS\nWhite/Gray/Black State Machine\nTraps & Isolates Back-Edges", Inches(3.8)),
        ("Stage 3: Topological Scheduler", "Kahn's In-Degree Queue BFS\nResolves Data Dependencies\nProduces Linear Order Array", Inches(6.8)),
        ("Stage 4: Execution & Verification", "Boolean Gate Switch Engine\nLevel-by-Level Signal Propagation\nExhaustive 2^N Truth Table", Inches(9.8))
    ]

    for title, desc, x_pos in stages:
        box = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, Inches(1.8), Inches(2.733), Inches(2.2))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(248, 250, 252)
        box.line.color.rgb = C_BLUE
        box.line.width = Pt(1.5)

        tb = s8.shapes.add_textbox(x_pos + Inches(0.1), Inches(1.9), Inches(2.533), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_SLATE
        p.alignment = PP_ALIGN.CENTER

    # Connectors between stages
    for arrow_x in [Inches(3.55), Inches(6.55), Inches(9.55)]:
        arr = s8.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arrow_x, Inches(2.7), Inches(0.23), Inches(0.4))
        arr.fill.solid()
        arr.fill.fore_color.rgb = C_BLUE
        arr.line.fill.background()

    # Bottom Architectural Detail Section
    tb_arch = s8.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.5))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p = tf_arch.paragraphs[0]
    p.text = "Pipeline Invariants & Execution Flow:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(6)

    flow_pts = [
        ("Invariant 1 (Strict Pre-Simulation Validation): ", "Execution is strictly blocked if Stage 2 detects a cycle. Feedback loops are halted with the exact back-edge reported, preventing infinite simulation loops."),
        ("Invariant 2 (Dependency Resolution Invariance): ", "Stage 3 guarantees that every gate in the execution array appears strictly after all its predecessor driver gates, eliminating race conditions in O(V + E) time."),
        ("Invariant 3 (Exhaustive Verification): ", "Stage 4 iterates across all 2^N input permutations, executing the circuit topologically and validating correctness against standard truth tables.")
    ]
    for bold_text, normal_text in flow_pts:
        p = tf_arch.add_paragraph()
        p.text = f"• {bold_text}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 9: 3. Algorithmic Novelty & Technical Contribution
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "3. Algorithmic Novelty", "Algorithmic Novelty & Technical Contribution", 9, 12)

    tb_s9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
    tf_s9 = tb_s9.text_frame
    tf_s9.word_wrap = True

    novelties = [
        ("1. Decoupled Dual-Phase Graph Validation", 
         "Standard simulators typically rely either on Kahn's algorithm alone (which fails blindly on cycles without reporting the fault location) or DFS alone (which does not provide a levelized forward execution queue). Our contribution decouples cycle diagnosis from evaluation scheduling: Tarjan's 3-Color DFS is used purely for cycle localization, while Kahn's algorithm is applied strictly to validated DAGs."),

        ("2. Dependency-Guaranteed Race-Free Execution in O(V + E)", 
         "In physical combinational circuits, signal race conditions occur when downstream gates calculate before upstream inputs settle. Our topological scheduler enforces strict dependency invariance, guaranteeing that every gate evaluates only after all its driver gates are resolved in linear O(V + E) time."),

        ("3. High-Performance O(1) Hash Map Gate Indexing", 
         "Rather than relying on continuous O(V) array scans, our simulator indexes gates, input pins, and wire nets via hash maps with unique string identifiers. This enables instant gate state updates and predecessor lookups during signal propagation."),

        ("4. Automated Exhaustive Bitwise Verification Engine", 
         "Implements an automated truth table generator evaluating all 2^N input vectors. Computes expected Boolean formulas against simulated outputs, achieving complete functional verification in milliseconds.")
    ]

    for idx, (title, desc) in enumerate(novelties):
        p = tf_s9.paragraphs[0] if idx == 0 else tf_s9.add_paragraph()
        p.text = title
        p.font.size = Pt(14.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.font.name = "Arial"
        p.space_after = Pt(2)

        p = tf_s9.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 10: 4. Algorithms / Pseudocode — Modules 1 & 2
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "4. Algorithms & Pseudocode", "Module 1 (Graph Netlist) & Module 2 (3-Color DFS Cycle Detection)", 10, 12)

    # Clean IEEE-style Algorithm Boxes (thin double border top/bottom)
    # Left: Module 1
    rule_m1_t = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.02))
    rule_m1_t.fill.solid()
    rule_m1_t.fill.fore_color.rgb = C_NAVY
    rule_m1_t.line.fill.background()

    tb_alg1 = s10.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(5.6), Inches(4.9))
    tf_alg1 = tb_alg1.text_frame
    tf_alg1.word_wrap = True

    p = tf_alg1.paragraphs[0]
    p.text = "Algorithm 1: Netlist Graph Construction"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    code_alg1 = """Input:  Gates V = {g_1, g_2, ...}, Wires E = {(u, v), ...}
Output: Adjacency list adjList, In-degree table inDegree

1:  adjList  = HashMap<GateID, List<GateID>>()
2:  inDegree = HashMap<GateID, Integer>()
3:  For each gate g in V do:
4:      adjList[g.id] = empty_list()
5:      inDegree[g.id] = 0
6:  End For
7:  For each wire (u, v) in E do:
8:      // u is driver gate, v is driven input
9:      adjList[u].append(v)
10:     inDegree[v] = inDegree[v] + 1
11: End For
12: Return (adjList, inDegree)

Complexity: O(V + E) time, O(V + E) space"""

    p = tf_alg1.add_paragraph()
    p.text = code_alg1
    p.font.size = Pt(10)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # Right: Module 2
    rule_m2_t = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(0.02))
    rule_m2_t.fill.solid()
    rule_m2_t.fill.fore_color.rgb = C_NAVY
    rule_m2_t.line.fill.background()

    tb_alg2 = s10.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(5.6), Inches(4.9))
    tf_alg2 = tb_alg2.text_frame
    tf_alg2.word_wrap = True

    p = tf_alg2.paragraphs[0]
    p.text = "Algorithm 2: Tarjan's 3-Color DFS Cycle Detection"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    code_alg2 = """Input:  Current gate u, Color map color, adjList
Output: Boolean (TRUE if cycle exists, FALSE otherwise)

1:  color[u] = GRAY  // Gate added to active recursion stack
2:  For each successor v in adjList[u] do:
3:      If color[v] == GRAY then:
4:          RecordCycleEdge(u, v)
5:          Return TRUE  // Back-edge found: Cycle trapped!
6:      End If
7:      If color[v] == WHITE then:
8:          If DetectCycle(v, color, adjList) == TRUE then:
9:              Return TRUE
10:         End If
11:     End If
12: End For
13: color[u] = BLACK // Subtree verified acyclic
14: Return FALSE

Complexity: O(V + E) time, O(V) recursion stack"""

    p = tf_alg2.add_paragraph()
    p.text = code_alg2
    p.font.size = Pt(10)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # =========================================================================
    # SLIDE 11: 4. Algorithms / Pseudocode — Modules 3 & 4
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_header(s11, "4. Algorithms & Pseudocode", "Module 3 (Kahn's Scheduler) & Module 4 (Logic Execution)", 11, 12)

    # Left: Module 3
    rule_m3_t = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.02))
    rule_m3_t.fill.solid()
    rule_m3_t.fill.fore_color.rgb = C_NAVY
    rule_m3_t.line.fill.background()

    tb_alg3 = s11.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(5.6), Inches(4.9))
    tf_alg3 = tb_alg3.text_frame
    tf_alg3.word_wrap = True

    p = tf_alg3.paragraphs[0]
    p.text = "Algorithm 3: Kahn's In-Degree Topo Scheduler"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    code_alg3 = """Input:  Gates V, In-degree table inDegree, adjList
Output: Topologically ordered execution list evalOrder

1:  Q = EmptyQueue()
2:  For each gate g in V do:
3:      If inDegree[g] == 0 then: Q.push(g)
4:  End For
5:  evalOrder = []
6:  While Q is not empty do:
7:      u = Q.pop()
8:      evalOrder.append(u)
9:      For each successor v in adjList[u] do:
10:         inDegree[v] = inDegree[v] - 1
11:         If inDegree[v] == 0 then: Q.push(v)
12:     End For
13: End While
14: Return evalOrder

Complexity: O(V + E) time, O(V) queue memory"""

    p = tf_alg3.add_paragraph()
    p.text = code_alg3
    p.font.size = Pt(10)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # Right: Module 4
    rule_m4_t = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(0.02))
    rule_m4_t.fill.solid()
    rule_m4_t.fill.fore_color.rgb = C_NAVY
    rule_m4_t.line.fill.background()

    tb_alg4 = s11.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(5.6), Inches(4.9))
    tf_alg4 = tb_alg4.text_frame
    tf_alg4.word_wrap = True

    p = tf_alg4.paragraphs[0]
    p.text = "Algorithm 4: Gate Simulation & Truth Table Engine"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(4)

    code_alg4 = """Algorithm SimulatePass(evalOrder, inputVector):
1:  values = HashMap<GateID, Boolean>()
2:  For each gate g in evalOrder do:
3:      If g.type == INPUT then:
4:          values[g.id] = inputVector[g.id]
5:      Else:
6:          inVals = [values[p] for p in g.predecessors]
7:          values[g.id] = EvaluateGateLogic(g.type, inVals)
8:      End If
9:  End For
10: Return values

Algorithm GenerateTruthTable(N_inputs, evalOrder):
1:  For row = 0 to (2^N - 1) do:
2:      inVec = DecodeBinaryRow(row, N_inputs)
3:      outVec = SimulatePass(evalOrder, inVec)
4:      PrintTruthTableRow(inVec, outVec)
5:  End For"""

    p = tf_alg4.add_paragraph()
    p.text = code_alg4
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_CODE_TEXT
    p.font.name = "Consolas"

    # =========================================================================
    # SLIDE 12: 5. Dataset & Benchmark Suite — IEEE ISCAS '85
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_slide_header(s12, "5. Dataset & Benchmark Suite", "IEEE ISCAS '85 Benchmark Circuit Suite", 12, 12)

    tb_s12_l = s12.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tf_s12_l = tb_s12_l.text_frame
    tf_s12_l.word_wrap = True

    p = tf_s12_l.paragraphs[0]
    p.text = "Benchmark Origin & Download Links"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"
    p.space_after = Pt(14)

    ds_pts_l = [
        ("Benchmark Suite: ", "IEEE ISCAS '85 (International Symposium on Circuits and Systems) Benchmark Suite."),
        ("Industry Standard Role: ", "The universally recognized reference standard in Electronic Design Automation (EDA) and academic CAD research for combinational circuit validation and test pattern generation."),
        ("Primary Repository Link: ", "University of Tennessee EECS CAD Lab:\nhttps://web.eecs.utk.edu/~troy/benchmark/"),
        ("Mirror Repository Link: ", "Czech Technical University (FEE CTU):\nhttps://ddd.fit.cvut.cz/prj/Benchmarks/"),
        ("Netlist File Syntax (.bench): ", "Human-readable ASCII grammar defining Primary Inputs (INPUT(x)), Primary Outputs (OUTPUT(y)), and logical equations (e.g., 10 = NAND(1, 3)).")
    ]
    for bold_text, normal_text in ds_pts_l:
        p = tf_s12_l.add_paragraph()
        p.text = f"• {bold_text}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(8)

    tb_s12_r = s12.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.1))
    tf_s12_r = tb_s12_r.text_frame
    tf_s12_r.word_wrap = True

    p = tf_s12_r.paragraphs[0]
    p.text = "Benchmark Netlists & Project Role"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.font.name = "Arial"
    p.space_after = Pt(14)

    bench_circuits = [
        ("c17 (6 Gates, 5 Inputs, 2 Outputs): ", "Smallest ISCAS netlist; used for fundamental sanity checks and exhaustive 32-row truth table verification against IEEE golden output specifications."),
        ("c432 (160 Gates, 36 Inputs, 7 Outputs): ", "27-channel interrupt controller; evaluates topological scheduling across medium-scale multi-fanout logic trees."),
        ("c499 (202 Gates, 41 Inputs, 32 Outputs): ", "32-bit single-error-correcting circuit (SEC-DED); verifies deep logic paths and XOR/NAND propagation."),
        ("c880 (383 Gates, 60 Inputs, 26 Outputs): ", "8-bit Arithmetic Logic Unit (ALU); validates linear O(V + E) runtime scaling and memory efficiency."),
        ("Validation Utility in Review: ", "Demonstrates algorithmic correctness against industry standard benchmarks rather than ad-hoc custom circuits.")
    ]
    for bold_text, normal_text in bench_circuits:
        p = tf_s12_r.add_paragraph()
        p.text = f"• {bold_text}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_SLATE
        p.font.name = "Arial"
        run = p.add_run()
        run.text = normal_text
        run.font.bold = False
        run.font.color.rgb = C_SLATE
        p.space_after = Pt(8)

    # Save presentation
    prs.save(output_pptx_path)
    print(f"Presentation saved successfully to: {output_pptx_path}")

if __name__ == "__main__":
    output_path = r"c:\Projects\DigitalLogicSimulator\Digital_Logic_Simulator_First_Review_Academic_V2.pptx"
    build_presentation(output_path)
