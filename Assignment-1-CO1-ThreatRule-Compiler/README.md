# ThreatRule Compiler Front-End

SIMATS Engineering · Compiler Design · Assignment 1 (CO1) · AUG–DEC 2026

This project contains a Flex-generated lexical analyzer for a small ThreatRule
language, test inputs, repeatable test/benchmark scripts, and the assignment
report. It is an educational defensive rule front-end; it does not execute
security actions.

## Requirements

- GCC and Flex (verified here: GCC 9.2.0, Flex 2.5.4)
- Python 3 for data generation and measurement; graph generation uses only the
  Python standard library
- Windows PowerShell, or a POSIX shell with `make`

## Build and run (Windows PowerShell)

From this directory:

```powershell
Push-Location LEX_Scanner
flex threatrule.l
gcc -std=c99 -O2 -Wall -Wextra -o ..\threatrule.exe lex.yy.c
Pop-Location
.\threatrule.exe Input_Files\sample_rule.tr
```

Token output is written to standard output; diagnostics are written to standard
error. `--quiet --stats` suppresses individual token lines and prints the
measured token/error/line counts, suitable for benchmarks. `--legacy` disables
the Day-4 hash/CVE/URL token rules to exercise the original design's limits.

Generate and run the test suites:

```powershell
python scripts\generate_inputs.py
python scripts\run_tests.py
python scripts\benchmark.py
python scripts\build_report_docx.py
```

The scripts build the scanner from the `.l` source before use. Benchmark
results are generated on the local machine and are not pre-filled or estimated.
The DOCX generator uses the `python-docx` dependency in `requirements.txt` and
Microsoft Edge to embed the original SVG diagrams as images.
See [the assignment report](Assignment_Document\Assignment_1_Report.md) and
[editable Word report](Assignment_Document\Assignment_1_Report.docx),
[faculty submission summary](SUBMISSION_SUMMARY.md), and
[traceability matrix](REQUIREMENT_TRACEABILITY.md) for scope and evidence.

## Portability

If Flex is missing on Windows, install a Windows Flex distribution (for
example, Flex in MSYS2 or WinFlexBison), add its executable directory to `PATH`,
and ensure the selected GCC toolchain is also on `PATH`. Reopen PowerShell and
verify `flex --version` and `gcc --version`. The `.l` source is the source of
truth; `lex.yy.c` is reproducibly generated and may vary by Flex version.

## Student fields

Student name, register number, class/section, signatures, and evaluation fields
are intentionally left blank/editable. No evaluation, signature, screenshot,
or performance result is fabricated in this repository.
