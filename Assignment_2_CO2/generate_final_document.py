from pathlib import Path
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent
WORD_DIR = ROOT / 'Word_Report'
PDF_DIR = ROOT / 'PDF_Report'
OUTPUT_DIR = ROOT / 'Output_Files'
WORD_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

sections = [
    ('Q1 - LL(1) Parsing Table Conflict', 'Source_Code/Q1/ll1_conflict_demo.py', OUTPUT_DIR / 'Q1_ll1_conflict.txt'),
    ('Q2 - Parse Tree Associativity', 'Source_Code/Q2/parse_tree_demo.py', OUTPUT_DIR / 'Q2_parse_tree.txt'),
    ('Q3 - Error Detection and Recovery', 'Source_Code/Q3/error_handling_demo.py', OUTPUT_DIR / 'Q3_error_handling.txt'),
    ('Q4 - Dangling Else Resolution', 'Source_Code/Q4/dangling_else_demo.py', OUTPUT_DIR / 'Q4_dangling_else.txt'),
    ('Q5 - Operator Precedence Conflict', 'Source_Code/Q5/operator_precedence_demo.py', OUTPUT_DIR / 'Q5_operator_precedence.txt'),
]

intro = [
    'Compiler Design Assignment 2 (CO2)',
    'This document summarizes the clean restart of the original scenario-based CO2 assignment and documents the verified outputs from the five parser-design tasks.',
    'The report is based on the original assessment paper in Question_Paper/AT2_SCENARIO_BASED_TASK.pdf and the actual execution evidence generated from the project source files.',
]

report_md = ['# Compiler Design Assignment 2 (CO2)', '',
             '## Introduction', '',
             'This document summarizes the clean restart of the original scenario-based CO2 assignment and records the actual execution evidence for the five parser-design tasks.',
             '',
             '## Table of Contents', '',
             '1. Q1 - LL(1) Parsing Table Conflict',
             '2. Q2 - Parse Tree Associativity',
             '3. Q3 - Error Detection and Recovery',
             '4. Q4 - Dangling Else Resolution',
             '5. Q5 - Operator Precedence Conflict',
             '6. Final Summary',
             '',
             '## Q1 - LL(1) Parsing Table Conflict', '']

for heading, code_path, output_file in sections:
    report_md.append(f'## {heading}')
    report_md.append('')
    report_md.append(f'Implementation source: `{code_path}`')
    report_md.append(f'Execution output: `{output_file.name}`')
    report_md.append('')
    report_md.append(output_file.read_text(encoding='utf-8'))
    report_md.append('')

report_md.append('## Final Summary')
report_md.append('')
report_md.append('All five scenario-based assignments were implemented, executed, and verified using the project output files in Output_Files/. The evidence confirms that the parser design issues were correctly identified, explained, and resolved by applying LL(1) validation, associativity fixes, recovery strategies, nearest-then rules, and precedence-based grammar redesign.')
report_md_text = '\n'.join(report_md)
(WORD_DIR / 'Assignment_2_CO2_Final_Report.md').write_text(report_md_text, encoding='utf-8')

# Create DOCX
word_document = Document()
word_document.styles['Normal'].font.name = 'Times New Roman'
word_document.styles['Normal'].font.size = 12
word_document.add_heading('Compiler Design Assignment 2 (CO2)', 0)
for para in intro:
    word_document.add_paragraph(para)
word_document.add_paragraph('Table of Contents')
for item in ['Q1 - LL(1) Parsing Table Conflict', 'Q2 - Parse Tree Associativity', 'Q3 - Error Detection and Recovery', 'Q4 - Dangling Else Resolution', 'Q5 - Operator Precedence Conflict', 'Final Summary']:
    word_document.add_paragraph(item)

for heading, code_path, output_file in sections:
    word_document.add_heading(heading, level=1)
    word_document.add_paragraph(f'Implementation source: {code_path}')
    word_document.add_paragraph(f'Execution output file: {output_file.name}')
    output_text = output_file.read_text(encoding='utf-8')
    # break long text into paragraphs to keep the document readable
    for line in output_text.splitlines():
        if line.strip():
            word_document.add_paragraph(line)

word_document.add_heading('Final Summary', level=1)
word_document.add_paragraph('All five scenario-based assignments were implemented, executed, and verified using the project output files in Output_Files/. The evidence confirms that the parser design issues were correctly identified, explained, and resolved by applying LL(1) validation, associativity fixes, recovery strategies, nearest-then rules, and precedence-based grammar redesign.')
word_document.save(WORD_DIR / 'Assignment_2_CO2_Final_Report.docx')

# Create PDF
pdf_path = PDF_DIR / 'Assignment_2_CO2_Final_Report.pdf'
styles = getSampleStyleSheet()
story = []
story.append(Paragraph('Compiler Design Assignment 2 (CO2)', styles['Title']))
story.append(Spacer(1, 12))
for line in intro:
    story.append(Paragraph(line, styles['BodyText']))
    story.append(Spacer(1, 8))
for heading, code_path, output_file in sections:
    story.append(Paragraph(heading, styles['Heading2']))
    story.append(Paragraph(f'Implementation source: {code_path}', styles['BodyText']))
    story.append(Paragraph(f'Execution output file: {output_file.name}', styles['BodyText']))
    for line in output_file.read_text(encoding='utf-8').splitlines():
        if line.strip():
            story.append(Paragraph(line, styles['BodyText']))
    story.append(Spacer(1, 10))
story.append(Paragraph('Final Summary', styles['Heading2']))
story.append(Paragraph('All five scenario-based assignments were implemented, executed, and verified using the project output files in Output_Files/. The evidence confirms that the parser design issues were correctly identified, explained, and resolved by applying LL(1) validation, associativity fixes, recovery strategies, nearest-then rules, and precedence-based grammar redesign.', styles['BodyText']))

doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, title='Compiler Design Assignment 2 (CO2)')
doc.build(story)

print('Generated Word report:', WORD_DIR / 'Assignment_2_CO2_Final_Report.docx')
print('Generated PDF report:', pdf_path)
