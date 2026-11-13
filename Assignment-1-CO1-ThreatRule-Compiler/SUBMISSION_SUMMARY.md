# Assignment 1 — Faculty Submission Summary

**Course:** Compiler Design, Unit I — Assignment 1 (CO1)  
**Project:** ThreatRule Compiler Front-End using LEX/Flex  
**Student:** ______________________________  
**Register number:** ______________________________  
**Faculty:** Dr. N. Deepa

## Work submitted

- Flex-based C lexical analyzer for ThreatRule, with line-numbered tokens,
  IPv4/port validation, symbol-table insertion, and recoverable lexical errors.
- Day-4 token support for MD5/SHA-1/SHA-256-shaped hashes, CVE identifiers, and
  documented HTTP(S) URLs.
- Academic report in Markdown and editable Word format, original diagrams,
  test cases and execution evidence, benchmark data and graphs, and viva
  questions.

## Verification performed

- Flex 2.5.4 generated the scanner; GCC 9.2.0 compiled it successfully.
- All seven automated test groups passed, including valid/invalid input,
  boundaries, empty input, live-feed tokens, and recovery after errors.
- Actual generated datasets of 100, 1,000, 10,000, and 100,000 rules were
  benchmarked. The 100,000-rule run recognized 1,800,000 tokens with zero
  lexical errors.
- The measured timings and environment are documented in
  `Performance_Analysis/performance_report.md`; timings include process startup
  and file I/O and are machine-dependent.

## Scope note

This submission implements and tests the lexical analyzer. A grammar parser,
complete semantic analysis, IR optimizer, and target-code generator are not
implemented; their report examples are identified as illustrative. The
`--legacy` feed comparison is a compatibility simulation, not a separately
preserved original scanner.

**Git commit:** ______________________________  
**Faculty evaluation / marks:** ______________________________
