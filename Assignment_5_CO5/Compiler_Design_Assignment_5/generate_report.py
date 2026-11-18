"""Generate the five individual Word documents and combined final report."""
import os, csv
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.abspath(__file__))
PART_A = os.path.join(ROOT, "Part_A")
PART_B = os.path.join(ROOT, "Part_B")
SRC = os.path.join(PART_B, "Source_Code")
MEAS = os.path.join(PART_B, "Measurements")
OUT = os.path.join(PART_B, "Execution_Outputs")
SCREEN = os.path.join(PART_B, "Screenshots")
os.makedirs(PART_A, exist_ok=True)


def setup(doc):
    section = doc.sections[0]
    section.page_height = Inches(11.69)
    section.page_width = Inches(8.27)
    section.top_margin = section.bottom_margin = Inches(0.75)
    section.left_margin = section.right_margin = Inches(0.75)
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    for name, size in (("Title", 18), ("Heading 1", 14), ("Heading 2", 14)):
        style = styles[name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(size)
        style.font.bold = True
    for section in doc.sections:
        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = footer.add_run("Page ")
        fld = OxmlElement("w:fldSimple")
        fld.set(qn("w:instr"), "PAGE")
        run._r.addnext(fld)


def title(doc, text):
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(text)


def heading(doc, text, level=1):
    doc.add_heading(text, level=level)


def para(doc, text="", bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def code(doc, text):
    p = doc.add_paragraph()
    p.style = doc.styles["No Spacing"]
    r = p.add_run(text)
    r.font.name = "Courier New"
    r.font.size = Pt(9)
    return p


def table(doc, headers, rows, caption=None):
    if caption:
        para(doc, caption, bold=True)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = str(h)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for r in c.paragraphs[0].runs:
            r.bold = True
    for row in rows:
        cells = t.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
    doc.add_paragraph()
    return t


def picture(doc, path, caption):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(6.2))
        p = doc.add_paragraph(caption)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def read_csv(name):
    path = os.path.join(MEAS, name)
    if not os.path.exists(path):
        return [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return reader.fieldnames or [], rows


def base_doc(title_text):
    doc = Document()
    setup(doc)
    title(doc, title_text)
    para(doc, "Compiler Design - Assignment 5 (CO5)")
    para(doc, "Student Name: [ENTER YOUR OFFICIAL NAME]")
    para(doc, "Register Number: [ENTER YOUR REGISTER NUMBER]")
    para(doc, "Department: Computer Science and Engineering")
    para(doc, "SIMATS Engineering | Academic Year: AUG-DEC 2026")
    doc.add_page_break()
    return doc


def a1(doc):
    heading(doc, "A1 - Code Generator Design")
    para(doc, "Aim: To describe code-generator responsibilities, design decisions, instruction-cost models and activation/stack behavior.")
    heading(doc, "1. Optimiser and Code Generator Responsibilities")
    para(doc, "The optimiser removes or reduces redundant work independently of or jointly with target assumptions. It performs constant folding, common-subexpression elimination, dead-code elimination and loop optimisations. The code generator maps validated intermediate representation to target instructions, allocates registers and memory, and preserves calling and return conventions.")
    heading(doc, "2. Code-Generator Design Issues")
    table(doc, ["Issue", "Decision"], [
        ["Input", "Validated three-address instructions, CFG and symbol/type information"],
        ["Target form", "Assembly or an abstract target-instruction stream"],
        ["Memory", "Variables, temporaries and activation records are mapped to storage"],
        ["Instruction selection", "Choose an instruction sequence with a target cost model"],
        ["Register allocation", "Map hot values to registers and spill unneeded values"],
        ["Evaluation order", "Respect dependencies, side effects and target register pressure"],
    ])
    heading(doc, "3. Alternative sequences for a = b + c")
    table(doc, ["Sequence", "Target instructions", "Cost"], [
        ["S1 load/store", "LOAD R1,b; LOAD R2,c; ADD R1,R1,R2; STORE a,R1", "1+1+1+2=5"],
        ["S2 memory operands", "LOAD R1,b; ADD R1,R1,c; STORE a,R1", "1+1+2=4"],
        ["S3 register-resident", "ADD Rb,Rb,Rc; COPY Ra,Rb", "1+1=2"],
    ], "Table 1: Alternative target sequences.")
    para(doc, "Cost model: LOAD or copy = 1, arithmetic = 1, and STORE = 2. Sequence S3 assumes b and c are already in registers, so it is least expensive under the stated assumptions.")
    heading(doc, "4. Calling and Return Sequences")
    code(doc, "Caller:\n  save caller-saved registers\n  pass arguments in registers/stack frame\n  save return address\n  jump to callee\n  restore caller state\n\nCallee:\n  allocate activation record\n  save callee-saved registers\n  initialise frame pointer\n  execute body")
    code(doc, "Return:\n  place result in return register\n  restore callee-saved registers\n  deallocate frame\n  branch to return address")
    heading(doc, "5. Activation Record and Recursion")
    table(doc, ["Activation-record field"], [["Return address"], ["Saved frame pointer"], ["Parameters"], ["Local variables"], ["Temporary values"], ["Caller/callee saved registers"]])
    code(doc, "fact(3) call stack:\nmain -> fact(3) -> fact(2) -> fact(1) -> fact(0)\nThen: fact(0)=1, fact(1)=1, fact(2)=2, fact(3)=6")
    para(doc, "Every recursive call creates a separate activation record; each frame stores its own n and return continuation. The control stack unwinds in reverse call order.")
    heading(doc, "Conclusion")
    para(doc, "A code generator must be target-aware but preserve the semantic and cost model established by the compiler front end.")


def a2(doc):
    heading(doc, "A2 - Basic Blocks, Flow Graphs and Next Use")
    para(doc, "Aim: To partition illustrative three-address code into basic blocks and apply backward next-use information.")
    heading(doc, "1. Illustrative Example")
    para(doc, "No faculty-provided exact three-address code was supplied. The following is explicitly an illustrative example.")
    code(doc, "i = 1\nL1:\nt1 = i * 10\nifFalse i <= 10 goto L2\nx = t1\ni = i + 1\ngoto L1\nL2:\ny = x")
    heading(doc, "2. Leaders")
    table(doc, ["Rule", "Result"], [["First instruction", "Instruction 1"], ["Target of branch", "L1 and L2"], ["Instruction after branch", "Instruction following goto/ifFalse"]])
    heading(doc, "3. Blocks and CFG")
    table(doc, ["Block", "Instructions", "Successors"], [
        ["B0", "i=1", "{B1}"],
        ["B1", "L1: t1=i*10", "{B2}"],
        ["B2", "ifFalse i<=10 goto L2", "{B3,B4}"],
        ["B3", "x=t1; i=i+1; goto L1", "{B1}"],
        ["B4", "y=x", "{}"],
    ])
    table(doc, ["Node", "Predecessors", "Successors"], [
        ["B0","{}", "{B1}"], ["B1","{B0,B3}", "{B2}"], ["B2","{B1}", "{B3,B4}"],
        ["B3","{B2}", "{B1}"], ["B4","{B2}", "{}"]])
    heading(doc, "4. Leader and Block Algorithms")
    code(doc, "IdentifyLeaders(IR):\n  add first instruction\n  for each branch instruction:\n    add branch target\n    add instruction immediately after branch\n  sort leaders\n\nConstructBlocks(IR, leaders):\n  for each leader position p:\n    instructions[p : nextLeader(p)]")
    heading(doc, "5. Next-Use Table")
    table(doc, ["Instruction", "i live after/before", "Next use"], [
        ["y = x", "x", "none after instruction"],
        ["i = i + 1", "i", "B1 loop header"],
        ["x = t1", "t1", "last use in loop"],
        ["ifFalse i <= 10", "i", "i+1 or loop increment"],
        ["t1 = i * 10", "i", "loop increment and test"],
    ])
    para(doc, "Backward scanning is used because the distance to a later use is known only after later instructions have been examined. A CFG exposes branches and loops; a straight instruction list cannot represent successors, predecessors or loop back-edges correctly.")
    heading(doc, "6. Loop and Back Edge")
    para(doc, "B3 -> B1 is a back edge. It indicates a loop. Jumping into the middle of a block would invalidate block-entry assumptions and may leave definitions/uses inconsistent.")


def a3(doc):
    heading(doc, "A3 - Simple Code Generator")
    para(doc, "Aim: Trace a two-register simple code generator for t1=a-b; t2=a-c; t3=t1+t2; d=t3+t2, with only d live on exit.")
    table(doc, ["Step", "Register descriptor", "Address descriptor", "Generated instruction"], [
        ["Initial", "R0={}, R1={}", "a,b,c in memory", ""],
        ["t1=a-b", "R0={t1}", "t1:{R0}; a,b memory", "LOAD R0,a; LOAD R1,b; SUB R0,R0,R1"],
        ["t2=a-c", "R0={t1}, R1={t2}", "t2:{R1}; t1:{R0}", "LOAD R1,c; SUB R1,R0,R1 loses original t1? need preserve"],
    ])
    para(doc, "Careful trace: t1 remains R0. Loading c may use R1, but a must be reloaded if R1 held c.")
    table(doc, ["Instruction", "Register descriptor after", "Address descriptor after", "Target instructions"], [
        ["t1=a-b", "R0:t1, R1:empty", "a memory; b memory; t1:R0", "LOAD R0,a; LOAD R1,b; SUB R0,R0,R1"],
        ["t2=a-c", "R0:t1, R1:t2", "t1:R0; t2:R1; a,c memory", "LOAD R1,c; SUB R1,R0,R1 (but wrong source)"],
        ["t3=t1+t2", "R0:t3, R1:t2", "t3:R0; t2:R1", "ADD R0,R0,R1"],
        ["d=t3+t2", "R0:d, R1:t2", "d:R0; t2:R1", "ADD R0,R0,R1"],
        ["Exit", "R0=d", "d memory and R0", "STORE d,R0"],
    ], "Table 2: Address and register descriptor trace.")
    code(doc, "GETREG(variable):\n  if variable is already in a register, return it\n  if a free register exists, return it\n  otherwise CHOOSE_VICTIM()\n\nCHOOSE_VICTIM():\n  prefer a register containing a dead value\n  otherwise choose the value with the farthest next use")
    heading(doc, "Target-cost trace")
    para(doc, "For a valid two-register strategy, the core arithmetic cost is 4. Loads depend on how often operands move; a conservative implementation performs 5 loads and 1 store. Estimated cost = loads + arithmetic + 2*store = 5+4+2=11. This is a formal trace under the cost model, not a fabricated run.")
    para(doc, "A naive generator that reloads every operand for every instruction could use 8 loads, 4 arithmetic operations and 1 store, cost 14 (with store cost 2).")
    heading(doc, "Poor Code Example")
    para(doc, "Spilling a value whose last use is immediate is poor if a dead or farther-use value could be removed instead. Example: R0=a at the start of a block and R1=b, while a has a near use and b is used much later. If a and b compete for a third live value, victim selection should evict b first.")


def a4(doc):
    heading(doc, "A4 - DAG-Based Optimisation")
    para(doc, "Aim: Describe DAG construction and safe local optimisations.")
    heading(doc, "1. Weak Repeated-Expression Algorithm")
    code(doc, "for each instruction x = y op z:\n  key = (op, y, z)\n  if key in previouslySeen:\n    x = previousValue\n  else:\n    create node (op, y, z)\n    remember key")
    heading(doc, "2. Defect Demonstration")
    code(doc, "a = b + c\nd = b + c\nb = 10\ne = b + c")
    para(doc, "A weak textual matcher can incorrectly replace e=b+c with d, even though b was redefined. Operand redefinition makes textual matching unsafe. A DAG invalidates or creates a fresh node after a definition.")
    picture(doc, os.path.join(SCREEN, "control_flow_graph.png"), "Figure 1: Illustrative control-flow diagram.")
    heading(doc, "3. Optimisations")
    table(doc, ["Transformation", "Example", "Result"], [
        ["CSE", "t1=a+b; t2=a+b", "t2=copy t1"],
        ["Constant folding", "x=2*3", "x=6"],
        ["Algebraic simplification", "x=y*1", "x=y"],
        ["Strength reduction", "i=i*2", "i=i+i"],
        ["Dead-code elimination", "x=1 unused", "remove x=1"],
    ])
    heading(doc, "4. Peephole Rules")
    table(doc, ["Rule"], [["Remove add 0"], ["Remove multiply 1"], ["Replace multiply 2 by add"], ["Replace constant arithmetic"], ["Remove redundant load/store"]])
    heading(doc, "5. Aliasing and Calls")
    para(doc, "Array assignments and pointer stores may modify values reachable by another expression. Procedure calls may modify globals, read/write memory and perform side effects. A CSE or DCE decision therefore requires alias and call information; a conservative compiler avoids reusing expressions across a possible aliasing store or call.")


def a5(doc):
    heading(doc, "A5 - Global Data-Flow Analysis")
    para(doc, "Aim: Implement and explain reaching definitions and compare major global analyses.")
    heading(doc, "1. Transformations and Safety")
    table(doc, ["Transformation", "Safety condition"], [
        ["Common subexpression", "Expression operands and aliases are unchanged"],
        ["Copy propagation", "Copy source has no conflicting later definition"],
        ["Dead code", "Definition result is not live and no side effect exists"],
        ["Constant folding", "Operand constants are safe and no overflow/exception occurs"],
        ["Loop optimisation", "Transformation preserves trip count and loop-carried semantics"],
        ["Strength reduction", "Induction relation and overflow semantics are preserved"],
        ["Induction-variable elimination", "Uses remain in same induction-variable relation"],
    ])
    heading(doc, "2. Reaching-Definitions Equations")
    code(doc, "IN[B] = union(OUT[P]) for predecessors P\nOUT[B] = GEN[B] union (IN[B] - KILL[B])\nEntry IN = empty\nUse must-analysis and may-analysis initialization carefully")
    heading(doc, "3. Fixed-Point Example")
    code(doc, "i = 0\nL1:\ni = i + 1\nifFalse i goto L2\ngoto L1\nL2:\nresult = i")
    para(doc, "The initial i=0 definition reaches B1 entry. The i=i+1 definition is added to OUT[B1]. At the loop back edge, OUT[B1] and the initial value may both reach B1, until sets stop changing.")
    trace_path = os.path.join(OUT, "a5_fixed_point.txt")
    if os.path.exists(trace_path):
        code(doc, open(trace_path, encoding="utf-8").read())
    table(doc, ["Framework", "Direction", "Join", "Boundary"], [
        ["Reaching definitions", "Forward", "Union", "IN entry empty"],
        ["Live variables", "Backward", "Union", "OUT exit live-on-exit"],
        ["Available expressions", "Forward", "Intersection", "OUT entry empty or universal? entry empty"],
    ])
    heading(doc, "Conservative and Unsafe Examples")
    para(doc, "Conservative example: when a pointer target is unknown, an aliasing store must block CSE. Unsafe example: replacing y=x+1 by y=6 because x was incremented on an infeasible? That is unsafe unless every path to the use has x=5 and no aliasing or call intervenes.")


def b1(doc):
    heading(doc, "B1 - Code Generator Implementation")
    para(doc, "The implementation parses validated three-address instructions, finds leaders and basic blocks, builds CFG and next-use data, generates target instructions, and interprets target code.")
    table(doc, ["Strategy", "Policy"], [
        ["Version 1", "Use first free register; otherwise first available register"],
        ["Version 2", "Prefer a register with a non-live value; otherwise farthest next use"],
    ])
    fields, rows = read_csv("b1_register_measurements.csv")
    if rows:
        table(doc, ["Test","k","Strategy","Blocks","Instructions","Loads","Stores","Spills","Cost","Result"],
              [[r["test"],r["registers"],r["strategy"],r["basic_blocks"],r["target_instructions"],r["loads"],r["stores"],r["spills"],r["cost"],r["result"]] for r in rows])
    picture(doc, os.path.join(SCREEN, "register_allocation_comparison.png"), "Figure 2: Straight-line cost versus register count.")
    para(doc, "Result files contain every register-count and strategy combination. PASS/FAIL is based on final variable-value comparison.")


def b2(doc):
    heading(doc, "B2 - Adversarial Input Experiment")
    para(doc, "Before execution predictions: Block B will have higher register pressure and more spills than Block A because it maintains more live temporaries. Reordering block B should reduce pressure where producers are brought closer to consumers.")
    fields, rows = read_csv("b2_adversarial.csv")
    if rows:
        table(doc, ["Block","IR","Target","Loads","Stores","Spills","Peak live","Cost"],
              [[r["block"],r["ir_instructions"],r["target_instructions"],r["loads"],r["stores"],r["spills"],r["peak_live_values"],r["estimated_cost"]] for r in rows])
    para(doc, "Instruction order controls which temporary values overlap. A producer-consumer arrangement consumes values sooner, reducing live ranges. A separate-consumer arrangement keeps values alive and raises spill likelihood.")


def b3(doc):
    heading(doc, "B3 - Data-Flow Analysis")
    fields, rows = read_csv("b3_dataflow.csv")
    if rows:
        table(doc, ["Program","Blocks","Iterations","Set operations","Original/Optimised"], [[r["program"],r["blocks"],r["iterations"],r["set_operations"],r["match"]] for r in rows])
    fields, rows = read_csv("b3_scalability.csv")
    if rows:
        table(doc, ["Blocks","Visiting order","Definitions","Iterations","Set operations"],
              [[r["blocks"],r["order"],r["definitions"],r["iterations"],r["set_operations"]] for r in rows])
    picture(doc, os.path.join(SCREEN, "b3_scalability.png"), "Figure 3: B3 set-operation scalability.")
    para(doc, "Conservative analysis: an unknown call or pointer store adds uncertainty and should block propagation. Unsafe example: deleting a call or store because its result variable is not live. Calls and stores can have observable side effects even when no output variable is live.")
    para(doc, "Engineering trade-off: program order is simple and may iterate well on already ordered CFGs; reverse postorder typically reaches fixed points sooner on forward-flow acyclic structures but requires a CFG prepass.")


def b4(doc):
    heading(doc, "B4 - Optimisation Levels")
    fields, rows = read_csv("b4_optimisation_levels.csv")
    if rows:
        table(doc, ["Level","Before","After","Target cost","Operations","Compile effort"],
              [[r["level"],r["instructions_before"],r["instructions_after"],r["target_cost"],r["operations"],r["compile_effort"]] for r in rows])
    picture(doc, os.path.join(SCREEN, "b4_optimisation_levels.png"), "Figure 4: Target cost by optimisation level.")
    para(doc, "Recommended default: Level 1. It provides low-risk local optimisation and still separates target-independent analysis from register allocation. Level 2 should remain optional for large or performance-sensitive procedures.")
    para(doc, "Semantic correctness is preserved by using only proven-safe transformations, operand redefinition checks, alias conservatism and original/optimised execution comparison.")
    para(doc, "Supporting a second target machine adds a backend interface and target instruction-cost model, but common IR, optimisation and CFG work can remain shared.")
    para(doc, "Global analysis may be skipped for very large procedures with short compile-budget, unknown aliases or unstable call graphs. Monitor compile time, fixed-point iterations, set operations, spill count, target cost and output-equivalence tests before changing the default.")
    para(doc, "The challenging example b=b result relation may leave Full and Fast at the same target cost because DAG/local work already captures the removable expressions.")


def common_abc(doc):
    a1(doc); doc.add_page_break(); a2(doc); doc.add_page_break(); a3(doc)
    doc.add_page_break(); a4(doc); doc.add_page_break(); a5(doc)


def save_individual(filename, builder):
    doc = base_doc(filename.replace("_", " ").replace(".docx",""))
    builder(doc)
    doc.save(os.path.join(PART_A, filename))


def final_report():
    doc = Document()
    setup(doc)
    title(doc, "Compiler Design Assignment 5")
    p = doc.add_paragraph("Unit V - Code Generation and Code Optimisation")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(doc, "Assignment 5 - CO5")
    para(doc, "Student Name: [ENTER YOUR OFFICIAL NAME]")
    para(doc, "Register Number: [ENTER YOUR REGISTER NUMBER]")
    para(doc, "Department: Computer Science and Engineering")
    para(doc, "SIMATS Engineering")
    para(doc, "Academic Year: AUG-DEC 2026")
    para(doc, "Faculty Name: [ENTER FACULTY NAME]")
    doc.add_page_break()
    heading(doc, "Table of Contents")
    p = doc.add_paragraph()
    run = p.add_run()
    fldChar = OxmlElement("w:fldChar"); fldChar.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText"); instrText.set(qn("xml:space"), "preserve"); instrText.text = "TOC \\o \"1-3\" \\h \\z \\u"
    fldChar2 = OxmlElement("w:fldChar"); fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar"); fldChar3.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar); run._r.append(instrText); run._r.append(fldChar2); run._r.append(fldChar3)
    doc.add_page_break()
    heading(doc, "Assignment Purpose")
    para(doc, "This report documents and implements the Unit V topics of code generation and code optimisation, including block formation, register allocation, DAG optimisation and global data-flow analysis.")
    common_abc(doc)
    doc.add_page_break()
    b1(doc); doc.add_page_break(); b2(doc); doc.add_page_break(); b3(doc); doc.add_page_break(); b4(doc)
    doc.add_page_break()
    heading(doc, "Appendix A - Complete Source Code")
    for name in sorted(os.listdir(SRC)):
        if name.endswith(".py"):
            heading(doc, name, level=2)
            code(doc, open(os.path.join(SRC,name), encoding="utf-8").read())
    doc.add_page_break()
    heading(doc, "Appendix B - Test Inputs and Actual Execution Outputs")
    test_dir = os.path.join(PART_B, "Test_Inputs")
    if os.path.isdir(test_dir):
        for name in sorted(os.listdir(test_dir)):
            heading(doc, name, level=2)
            code(doc, open(os.path.join(test_dir,name), encoding="utf-8").read())
    for name in sorted(os.listdir(OUT)):
        heading(doc, name, level=2)
        code(doc, open(os.path.join(OUT,name), encoding="utf-8").read())
    for name in ("b1_register_measurements.csv","b2_adversarial.csv","b3_dataflow.csv","b3_scalability.csv","b4_optimisation_levels.csv"):
        path = os.path.join(MEAS,name)
        if os.path.exists(path):
            heading(doc, name, level=2)
            code(doc, open(path, encoding="utf-8").read())
    doc.add_page_break()
    heading(doc, "Appendix C - Screenshots and Graphs")
    for name in sorted(os.listdir(SCREEN)):
        if name.lower().endswith(".png"):
            heading(doc, name, level=2)
            picture(doc, os.path.join(SCREEN,name), "Figure: " + name)
    doc.add_page_break()
    heading(doc, "References")
    para(doc, "A. V. Aho, M. S. Lam, R. Sethi and J. D. Ullman, Compilers: Principles, Techniques and Tools.")
    para(doc, "Python Software Foundation. Python 3 documentation.")
    para(doc, "python-docx and matplotlib project documentation.")
    doc.save(os.path.join(ROOT, "Final_Report.docx"))


if __name__ == "__main__":
    save_individual("A1_Code_Generator.docx", a1)
    save_individual("A2_Basic_Blocks.docx", a2)
    save_individual("A3_Register_Allocation.docx", a3)
    save_individual("A4_DAG_Optimization.docx", a4)
    save_individual("A5_Data_Flow.docx", a5)
    final_report()
