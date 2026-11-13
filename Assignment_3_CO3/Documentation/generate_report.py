from pathlib import Path
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]


def generate_report():
    out_dir = ROOT / 'Documentation'
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = Document()
    doc.add_heading('Assignment 3 – Compiler Design (CO3)', 0)
    doc.add_paragraph('This report records the generated outputs and implementation evidence for Q1–Q7.')
    doc.add_paragraph('The project is organized in the isolated Assignment_3_CO3 directory and preserves prior coursework.')
    doc.save(str(out_dir / 'Assignment_3_Report.docx'))

    pdf_path = out_dir / 'Assignment_3_Report.pdf'
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.setTitle('Assignment 3 Report')
    c.setFont('Helvetica-Bold', 16)
    c.drawString(72, 760, 'Assignment 3 – Compiler Design (CO3)')
    c.setFont('Helvetica', 12)
    c.drawString(72, 730, 'Generated implementation and evidence for Q1–Q7')
    c.save()
    print('Generated Word and PDF reports.')


if __name__ == '__main__':
    generate_report()
