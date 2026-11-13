"""Convert the assignment Markdown report into an editable, illustrated DOCX."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Assignment_Document"
REPORT = DOCS / "Assignment_1_Report.md"
OUTPUT = DOCS / "Assignment_1_Report.docx"
EDGE_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)
INLINE_PATTERN = re.compile(r"(\*\*.*?\*\*|`.*?`|\*.*?\*|\[[^\]]+\]\([^)]+\))")
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def set_cell_shading(cell, fill: str) -> None:
    properties = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    properties.append(shading)


def set_cell_text(cell, text: str, *, header: bool = False) -> None:
    cell.text = ""
    paragraph = cell.paragraphs[0]
    add_inline(paragraph, text, base_size=9)
    if header:
        for run in paragraph.runs:
            run.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_shading(cell, "23446B")
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_hyperlink(paragraph, label: str, target: str) -> None:
    relationship = paragraph.part.relate_to(
        target,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    properties.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.append(underline)
    run.append(properties)
    text = OxmlElement("w:t")
    text.text = label
    run.append(text)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def add_inline(paragraph, text: str, base_size: int = 12) -> None:
    cursor = 0
    for match in INLINE_PATTERN.finditer(text):
        if match.start() > cursor:
            paragraph.add_run(text[cursor : match.start()])
        token = match.group()
        link = LINK_PATTERN.fullmatch(token)
        if link:
            add_hyperlink(paragraph, link.group(1), link.group(2))
        elif token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(max(8, base_size - 1))
        else:
            run = paragraph.add_run(token[1:-1])
            run.italic = True
        cursor = match.end()
    if cursor < len(text):
        paragraph.add_run(text[cursor:])
    for run in paragraph.runs:
        if run.font.name != "Consolas":
            run.font.name = "Times New Roman"
        run.font.size = Pt(base_size)


def set_repeat_table_header(row) -> None:
    row_properties = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    row_properties.append(repeat)


def parse_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def find_edge() -> Path:
    for candidate in EDGE_CANDIDATES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Microsoft Edge is required to rasterize the report SVG diagrams.")


def svg_size(svg_path: Path) -> tuple[int, int]:
    text = svg_path.read_text(encoding="utf-8")
    match = re.search(r'<svg[^>]*viewBox="0 0\s+(\d+)\s+(\d+)"', text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 900, 600


def render_svg(svg_path: Path, png_path: Path, edge: Path, profile: Path) -> None:
    width, height = svg_size(svg_path)
    command = [
        str(edge),
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        f"--user-data-dir={profile}",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        svg_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    if result.returncode != 0 or not png_path.exists():
        raise RuntimeError(
            f"Could not render {svg_path.name} for Word: {result.stderr or result.stdout}"
        )


def add_page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run("Page ")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)


def add_cover(document: Document) -> None:
    for _ in range(2):
        document.add_paragraph()
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("SIMATS ENGINEERING")
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(35, 68, 107)

    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Department of Computer Science and Engineering")
    run.font.size = Pt(14)

    for _ in range(2):
        document.add_paragraph()
    for text, size, bold in (
        ("COMPILER DESIGN — UNIT I", 16, True),
        ("ASSIGNMENT 1 — CO1", 15, True),
        ("AUG–DEC 2026", 12, False),
    ):
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)

    document.add_paragraph()
    title = (
        "Development of a Domain-Specific Compiler Front-End using LEX for "
        "Federated Cyber Threat Detection in Security Operations Centers"
    )
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(15)

    for label, rows in (
        (
            "Student information",
            [
                ("Student name", "__________________________________"),
                ("Register number", "__________________________________"),
                ("Class / section", "__________________________________"),
                ("Submission date", "__________________________________"),
            ],
        ),
        (
            "Evaluation (faculty use)",
            [
                ("Faculty", "Dr. N. Deepa"),
                ("Marks awarded", "__________ / 50"),
                ("Evaluation date", "__________________________________"),
                ("Faculty signature", "__________________________________"),
                ("Student signature", "__________________________________"),
            ],
        ),
    ):
        p = document.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        run = p.add_run(label)
        run.bold = True
        table = document.add_table(rows=0, cols=2)
        table.style = "Table Grid"
        for left, right in rows:
            cells = table.add_row().cells
            cells[0].text = left
            cells[1].text = right
            for cell in cells:
                for paragraph in cell.paragraphs:
                    for cell_run in paragraph.runs:
                        cell_run.font.name = "Times New Roman"
                        cell_run.font.size = Pt(11)
    document.add_page_break()


def add_markdown(document: Document, markdown: str, edge: Path, asset_dir: Path) -> None:
    lines = markdown.splitlines()
    index = 0
    code_lines: list[str] | None = None
    image_counter = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("```"):
            if code_lines is None:
                code_lines = []
            else:
                p = document.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.space_after = Pt(7)
                run = p.add_run("\n".join(code_lines))
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                code_lines = None
            index += 1
            continue
        if code_lines is not None:
            code_lines.append(line)
            index += 1
            continue
        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            image_counter += 1
            source = (DOCS / image_match.group(2).replace("/", "\\" )).resolve()
            png = asset_dir / f"diagram_{image_counter:02d}.png"
            profile = asset_dir / f"profile_{image_counter:02d}"
            render_svg(source, png, edge, profile)
            paragraph = document.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.add_run().add_picture(str(png), width=Inches(6.4))
            shutil.rmtree(profile, ignore_errors=True)
            index += 1
            continue
        if stripped.startswith("|") and index + 1 < len(lines) and re.match(
            r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[index + 1]
        ):
            table_rows = [parse_table_row(stripped)]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_rows.append(parse_table_row(lines[index]))
                index += 1
            width = max(len(row) for row in table_rows)
            table = document.add_table(rows=0, cols=width)
            table.style = "Table Grid"
            table.autofit = True
            for row_number, values in enumerate(table_rows):
                cells = table.add_row().cells
                set_repeat_table_header(table.rows[0])
                for col in range(width):
                    set_cell_text(
                        cells[col],
                        values[col] if col < len(values) else "",
                        header=(row_number == 0),
                    )
            continue
        if not stripped or stripped == "---":
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = min(len(heading.group(1)), 3)
            paragraph = document.add_paragraph(style=f"Heading {level}")
            add_inline(paragraph, heading.group(2), base_size=14 if level == 1 else 12)
            paragraph.paragraph_format.keep_with_next = True
            index += 1
            continue
        if stripped.startswith(">"):
            paragraph = document.add_paragraph()
            paragraph.paragraph_format.left_indent = Inches(0.2)
            paragraph.paragraph_format.right_indent = Inches(0.2)
            add_inline(paragraph, stripped.lstrip("> ").strip())
            for run in paragraph.runs:
                run.italic = True
            index += 1
            continue
        if stripped.startswith("- "):
            paragraph = document.add_paragraph(style="List Bullet")
            add_inline(paragraph, stripped[2:])
            index += 1
            continue
        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            paragraph = document.add_paragraph(style="List Number")
            add_inline(paragraph, numbered.group(1))
            index += 1
            continue
        paragraph = document.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(5)
        paragraph.paragraph_format.line_spacing = 1.15
        add_inline(paragraph, stripped)
        index += 1


def main() -> None:
    report = REPORT.read_text(encoding="utf-8")
    edge = find_edge()
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    normal = document.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.space_after = Pt(5)
    for name in ("Heading 1", "Heading 2", "Heading 3"):
        style = document.styles[name]
        style.font.name = "Times New Roman"
        style.font.bold = True
        style.font.color.rgb = RGBColor(35, 68, 107)
    document.styles["Heading 1"].font.size = Pt(14)
    document.styles["Heading 2"].font.size = Pt(13)
    document.styles["Heading 3"].font.size = Pt(12)
    add_page_number(section.footer.paragraphs[0])

    add_cover(document)
    with tempfile.TemporaryDirectory(prefix="threatrule_docx_") as temporary:
        add_markdown(document, report, edge, Path(temporary))
        document.core_properties.title = (
            "ThreatRule Compiler Front-End — Assignment 1 Report"
        )
        document.core_properties.subject = "Compiler Design Assignment 1 CO1"
        document.core_properties.author = "SIMATS Engineering student"
        document.save(OUTPUT)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
