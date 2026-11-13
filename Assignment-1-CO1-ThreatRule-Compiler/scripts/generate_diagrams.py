"""Generate original, editable vector diagrams for the report."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Diagrams"
FONT = "Arial, sans-serif"


def box(
    x: int, y: int, w: int, h: int, label: str, fill: str = "#eaf1ff", font_size: int = 14
) -> str:
    lines = label.split("\n")
    text = "".join(
        f'<text x="{x + w / 2}" y="{y + 27 + index * 19}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="{font_size}">{escape(line)}</text>'
        for index, line in enumerate(lines)
    )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" '
        f'stroke="#244b80" stroke-width="2"/>{text}'
    )


def arrow(x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
    midx, midy = (x1 + x2) / 2, (y1 + y2) / 2
    title = (
        f'<text x="{midx}" y="{midy - 7}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12">{escape(label)}</text>'
        if label else ""
    )
    return (
        f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#333" stroke-width="2" '
        f'marker-end="url(#arrow)"/>{title}'
    )


def document(title: str, width: int, height: int, content: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="10" '
        f'markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" '
        f'fill="#333"/></marker></defs><rect width="100%" height="100%" fill="white"/>'
        f'<text x="{width/2}" y="30" text-anchor="middle" font-family="{FONT}" '
        f'font-weight="bold" font-size="19">{escape(title)}</text>{content}</svg>'
    )


def flow(name: str, title: str, labels: list[str], colors: list[str] | None = None) -> None:
    width, height, node_w, node_h, gap = 980, 175, 150, 62, 18
    total = len(labels) * node_w + (len(labels) - 1) * gap
    start = (width - total) // 2
    parts = []
    for i, label in enumerate(labels):
        x = start + i * (node_w + gap)
        parts.append(box(x, 68, node_w, node_h, label, (colors or [])[i] if colors else "#eaf1ff"))
        if i:
            parts.append(arrow(x - gap + 1, 99, x, 99))
    (OUT / name).write_text(document(title, width, height, "".join(parts)), encoding="utf-8")


def transition_diagrams() -> None:
    width, height = 760, 840
    content = []
    panels = [
        (40, "Relational operators", [
            "Start", "Read <, >, =, !", "Look ahead", "Accept <=, >=, ==, !=\nor retract <, >, ="
        ], ["< > = !", "optional =", "otherwise"]),
        (240, "Identifiers and keywords", [
            "Start", "Letter or _", "Consume letters,\ndigits, underscore", "Accept identifier;\nkeyword-table lookup"
        ], ["letter/_", "continue", "delimiter"]),
        (440, "Integers", [
            "Start", "Digit", "Consume digits", "Accept integer;\nretract delimiter"
        ], ["digit", "digit", "delimiter"]),
        (640, "IPv4 address", [
            "Start", "Read octet 1", "Read octets 2 and 3\nwith dots", "Read octet 4;\nvalidate 0..255"
        ], ["digit", "dot + digits", "dot + digits"]),
    ]
    for y, title, labels, edge_labels in panels:
        content.append(
            f'<text x="{width/2}" y="{y+20}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="16" font-weight="bold">{escape(title)}</text>'
        )
        node_w, node_h, step, start_x = 150, 70, 180, 30
        for i, label in enumerate(labels):
            nx = start_x + i * step
            node_y = y + 60
            content.append(box(nx, node_y, node_w, node_h, label, "#f1f6ff", 12))
            if i == len(labels) - 1:
                content.append(
                    f'<rect x="{nx+4}" y="{node_y+4}" width="{node_w-8}" height="{node_h-8}" '
                    'rx="5" fill="none" stroke="#244b80" stroke-width="1.5"/>'
                )
            if i:
                content.append(arrow(nx - (step - node_w), y + 95, nx, y + 95))
                content.append(
                    f'<text x="{nx-15}" y="{node_y-8}" text-anchor="middle" '
                    f'font-family="{FONT}" font-size="12">{escape(edge_labels[i-1])}</text>'
                )
    content.append(
        '<text x="30" y="820" font-family="' + FONT + '" font-size="12">'
        "Double border = accepting state. Flex uses longest match; nonmatching lookahead "
        "is retracted before accepting a shorter operator/token.</text>"
    )
    (OUT / "token_transition_diagrams.svg").write_text(
        document("ThreatRule token transition diagrams", width, height, "".join(content)),
        encoding="utf-8",
    )


def buffer_diagram() -> None:
    content = (
        box(40, 100, 250, 90, "Buffer 1\ninput characters ... sentinel") +
        box(350, 100, 250, 90, "Buffer 2\ninput characters ... sentinel") +
        box(670, 100, 250, 90, "Refill buffer\nwhen a sentinel is reached", "#fff4df") +
        arrow(290, 145, 350, 145, "scan forward") +
        arrow(600, 145, 670, 145, "sentinel") +
        arrow(795, 190, 160, 230, "alternate buffers; preserve lexeme start") +
        box(250, 280, 500, 70, "lexeme start pointer + forward pointer\nlookahead; retract at token boundary")
    )
    (OUT / "buffer_pair_and_sentinel.svg").write_text(
        document("Input buffering: paired buffers and sentinels", 960, 390, content),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    flow(
        "language_processing_system.svg",
        "ThreatRule language-processing system",
        ["ThreatRule\nsource", "Flex scanner\n+ parser", "compiler\nIR", "native SOC\nengine", "loader /\nSOC runtime"],
        ["#eaf1ff", "#d9ecff", "#e7f5e9", "#fff4df", "#f4eaff"],
    )
    flow(
        "compiler_phases.svg",
        "Compiler phases and shared structures",
        ["Source", "Lexical\nanalysis", "Syntax\nanalysis", "Semantic\nanalysis", "IR +\noptimization", "Target\ncode"],
    )
    flow(
        "frontend_backend.svg",
        "Front-end / back-end grouping",
        ["Front end:\nscan + parse", "Semantic\nanalysis", "IR boundary", "Back end:\noptimize", "Generate\nSOC target"],
    )
    flow(
        "threatrule_architecture.svg",
        "ThreatRule educational compiler architecture",
        ["Source text", "Flex lexer\n(tokens + errors)", "symbol table", "Parser + semantic\nchecks (design)", "IR / target\n(design)"],
    )
    flow(
        "scanner_parser_interaction.svg",
        "Scanner, parser, and symbol-table interaction",
        ["Source\ncharacters", "Scanner\nFlex tokens", "Parser\n(grammar)", "Symbol table\n(attributes)"],
    )
    flow(
        "testing_workflow.svg",
        "Reproducible scanner testing workflow",
        ["Generate\ninputs", "Flex\nthreatrule.l", "GCC\nlex.yy.c", "Run valid /\ninvalid tests", "CSV + SVG\nevidence"],
    )
    flow(
        "design_challenge_comparison.svg",
        "Day-4 design comparison",
        ["Original\nIPv4 + base tokens", "Unsupported\nHASH / CVE / URL", "Extended Flex\nrules + validation", "Enhanced tokens;\nline diagnostics"],
    )
    transition_diagrams()
    buffer_diagram()
    print(f"Generated original SVG diagrams under {OUT}")


if __name__ == "__main__":
    main()
