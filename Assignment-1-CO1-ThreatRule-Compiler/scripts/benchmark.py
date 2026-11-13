"""Measure the generated Flex scanner and create CSV plus SVG graphs."""

from pathlib import Path
import csv
import datetime
import platform
import re
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SCANNER_DIR = ROOT / "LEX_Scanner"
EXE = ROOT / "threatrule.exe"
CSV_PATH = ROOT / "Performance_Analysis" / "performance_results.csv"
SIZES = (100, 1_000, 10_000, 100_000)
STAT = re.compile(r"TOKENS=(\d+) ERRORS=(\d+) LINES=(\d+)")


def execute(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def hardware_metadata() -> list[str]:
    if platform.system() == "Windows":
        command = (
            "$cpu=(Get-CimInstance Win32_Processor | Select-Object -First 1 -ExpandProperty Name); "
            "$sys=Get-CimInstance Win32_ComputerSystem; "
            "Write-Output ('Processor: ' + $cpu); "
            "Write-Output ('System: ' + $sys.Manufacturer + ' ' + $sys.Model); "
            "Write-Output ('Physical memory (GiB): ' + "
            "[math]::Round($sys.TotalPhysicalMemory/1GB,1))"
        )
        result = execute(["powershell", "-NoProfile", "-Command", command], ROOT)
        if result.returncode == 0 and result.stdout.strip():
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return [f"Processor: {platform.processor() or platform.machine()}"]


def build() -> None:
    generated = execute(["flex", "threatrule.l"], SCANNER_DIR)
    if generated.returncode:
        raise RuntimeError(generated.stderr)
    compiled = execute(
        ["gcc", "-std=c99", "-O2", "-Wall", "-Wextra", "-o", str(EXE), "lex.yy.c"],
        SCANNER_DIR,
    )
    if compiled.returncode:
        raise RuntimeError(compiled.stderr)


def measure(path: Path, legacy: bool = False) -> dict[str, object]:
    command = [str(EXE), "--quiet", "--stats"]
    if legacy:
        command.append("--legacy")
    command.append(str(path))
    elapsed_values: list[float] = []
    result: subprocess.CompletedProcess[str] | None = None
    for _ in range(5):
        started = time.perf_counter()
        result = execute(command, ROOT)
        elapsed_values.append(time.perf_counter() - started)
        match = STAT.search(result.stdout)
        if not match:
            raise RuntimeError(f"No scanner statistics for {path}:\n{result.stderr}\n{result.stdout}")
        tokens, errors, lines = map(int, match.groups())
    elapsed = statistics.median(elapsed_values)
    line_count = sum(1 for _ in path.open(encoding="ascii"))
    is_rule_set = path.name.startswith("rules_")
    return {
        "benchmark_case": path.stem,
        "rules": line_count if is_rule_set else 0,
        "lines": lines,
        "tokens": tokens,
        "scanning_time_seconds": f"{elapsed:.9f}",
        "timed_repetitions": len(elapsed_values),
        "lexical_errors": errors,
        "throughput_rules_per_second": f"{(line_count / elapsed if is_rule_set else 0):.3f}",
        "scanner_mode": "original" if legacy else "enhanced",
        "process_exit_code": result.returncode,
    }


def write_graphs(rows: list[dict[str, object]]) -> None:
    directory = ROOT / "Graphs"
    directory.mkdir(exist_ok=True)
    measures = (
        ("scanning_time_seconds", "Scanning time (seconds)", "rules_vs_time.svg"),
        ("tokens", "Recognized tokens", "rules_vs_tokens.svg"),
        ("throughput_rules_per_second", "Throughput (rules/second)", "rules_vs_throughput.svg"),
        ("lexical_errors", "Lexical errors", "rules_vs_errors.svg"),
    )
    primary = [row for row in rows if row["scanner_mode"] == "enhanced"]
    for key, label, name in measures:
        values = [(int(row["rules"]), float(row[key])) for row in primary]
        width, height, margin = 760, 420, 70
        max_x = max(x for x, _ in values) or 1
        max_y = max((y for _, y in values), default=0) or 1
        points = []
        for index, (x, y) in enumerate(values):
            px = margin + (index / max(1, len(values) - 1)) * (width - 2 * margin)
            py = height - margin - (y / max_y) * (height - 2 * margin)
            points.append((px, py, x, y))
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="white"/>',
            f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="18">{label} vs rules</text>',
            f'<path d="M {margin} {margin} V {height-margin} H {width-margin}" fill="none" stroke="#333" stroke-width="2"/>',
            f'<text x="{width/2}" y="{height-18}" text-anchor="middle" font-family="Arial" font-size="14">Rules</text>',
            f'<text x="20" y="{height/2}" transform="rotate(-90 20 {height/2})" text-anchor="middle" font-family="Arial" font-size="14">{label}</text>',
        ]
        poly = " ".join(f"{px:.1f},{py:.1f}" for px, py, _, _ in points)
        if points:
            svg.append(f'<polyline points="{poly}" fill="none" stroke="#155eef" stroke-width="3"/>')
        for px, py, x, y in points:
            svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#155eef"/>')
            svg.append(f'<text x="{px:.1f}" y="{py-10:.1f}" text-anchor="middle" font-family="Arial" font-size="11">{y:g}</text>')
            svg.append(f'<text x="{px:.1f}" y="{height-margin+22}" text-anchor="middle" font-family="Arial" font-size="11">{x}</text>')
        svg.append("</svg>")
        (directory / name).write_text("\n".join(svg), encoding="utf-8")


def main() -> int:
    build()
    rows: list[dict[str, object]] = []
    for size in SIZES:
        path = ROOT / "Input_Files" / f"rules_{size}.tr"
        if not path.exists():
            raise RuntimeError(f"Missing generated input {path}; run scripts/generate_inputs.py first.")
        rows.append(measure(path))
    challenge = ROOT / "Input_Files" / "hash_cve_url_feed.tr"
    rows.append(measure(challenge, legacy=True))
    rows.append(measure(challenge))
    CSV_PATH.parent.mkdir(exist_ok=True)
    columns = list(rows[0].keys())
    with CSV_PATH.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    write_graphs(rows)
    gcc = execute(["gcc", "--version"], ROOT).stdout.splitlines()[0]
    flex = execute(["flex", "--version"], ROOT).stdout.strip()
    report = [
        "# Scanner performance report",
        "",
        f"Measurement date/time: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Operating system: {platform.platform()}",
        f"Architecture: {platform.machine()}",
        *hardware_metadata(),
        f"C compiler: {gcc}",
        f"Flex: {flex}",
        "Method: five fresh scanner processes per input; report the median wall-clock elapsed "
        "time measured with Python `time.perf_counter()`, including process startup and file "
        "I/O. Inputs are deterministically generated by `scripts/generate_inputs.py`. Counts "
        "come from the scanner's own counters; no estimated values are used.",
        "",
        "| Case | Rules | Lines (scanner counter) | Tokens | Median time (s) | Errors | Rules/s | Mode |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        report.append(
            "| {benchmark_case} | {rules} | {lines} | {tokens} | {scanning_time_seconds} | "
            "{lexical_errors} | {throughput_rules_per_second} | {scanner_mode} |".format(**row)
        )
    report += [
        "",
        "Challenge-feed cases have `rules=0`: those inputs are token samples rather than rule "
        "sets. The original mode intentionally rejects HASH, CVE, and URL lexemes. The "
        "enhanced mode recognizes the supported examples. The legacy nonzero process exit "
        "indicates reported lexical errors, not a crash.",
        "",
        "Graphs use only the four generated rule-set runs. Measurements are machine- and "
        "load-dependent; rerun the script before drawing performance conclusions.",
    ]
    (ROOT / "Performance_Analysis" / "performance_report.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(f"Recorded {len(rows)} actual runs in {CSV_PATH.relative_to(ROOT)}")
    for row in rows:
        print(row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
