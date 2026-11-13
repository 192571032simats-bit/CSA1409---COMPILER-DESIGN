# Requirement Traceability

Statuses reflect evidence currently present in this project. `VERIFIED` is used
only where the listed implementation and test/evidence exist; theoretical
examples and unimplemented stages are marked partial.

| Assignment task | Requirement | Implementation file | Test performed | Evidence file | Actual completion status |
|---|---|---|---|---|---|
| Task 1 | Compare processors, justify compiler, show system | `Assignment_Document/Assignment_1_Report.md`; `Diagrams/language_processing_system.svg` | Document/diagram inspected | Report and SVG | PARTIALLY VERIFIED |
| Task 2 | Apply all compiler phases to sample | Report phase examples; only lexer executable | Sample scanned; later phases not run | `Output_Files/token_output.txt` | PARTIALLY VERIFIED |
| Task 3 | Explain grouping, passes, architecture | Report; `Diagrams/frontend_backend.svg` | Document/diagram inspected | Report and SVG | PARTIALLY VERIFIED |
| Task 4 | Explain six construction-tool categories | Report | Document inspected | Report table | PARTIALLY VERIFIED |
| Task 5 | Whitespace/comments, line tracking, recovery and faults | `LEX_Scanner/threatrule.l` | Valid/invalid multi-line inputs scanned | `Output_Files/invalid_errors.txt`; `Diagrams/buffer_pair_and_sentinel.svg` | PARTIALLY VERIFIED |
| Task 6 | Define token patterns and validation | `LEX_Scanner/threatrule.l` | IPv4, port, hash/CVE/URL test runs | `Output_Files/boundary_errors.txt`; design-challenge token output | PARTIALLY VERIFIED |
| Task 7 | Transition diagrams and hand traces | `scripts/generate_diagrams.py` | SVG generated; traces described | `Diagrams/token_transition_diagrams.svg` | PARTIALLY VERIFIED |
| Task 8 | Complete compilable Flex specification | `LEX_Scanner/threatrule.l` | Flex generation and GCC compilation | `LEX_Scanner/lex.yy.c`; test report | PARTIALLY VERIFIED |
| Task 9 | Execute actual scanner tests and 4 dataset sizes | `scripts/run_tests.py`; `scripts/generate_inputs.py` | Valid, invalid, boundary, feed, legacy, empty input; 100/1k/10k/100k generated | `Test_Cases/test_results.md`; `Output_Files/` | VERIFIED |
| Task 10 | Measure scanner and generate CSV/graphs | `scripts/benchmark.py` | Five runs per case, median measured | `Performance_Analysis/performance_results.csv`; `Graphs/` | VERIFIED |
| Task 11 | Defend final design using observed results | Report and generated performance report | 100,000-rule dataset benchmarked | `Performance_Analysis/performance_report.md` | PARTIALLY VERIFIED |
| Task 12A | Analyze added token types and impacts | Report | Design documented | Report | PARTIALLY VERIFIED |
| Task 12B | Test original scanner support/diagnostics | `--legacy` mode in Flex source (compatibility simulation, not old source) | Feed scanned in legacy and enhanced modes | `Output_Files/design_challenge_legacy_errors.txt` | PARTIALLY VERIFIED |
| Task 12C | Recognize hashes, CVEs, URLs; continue after errors | `LEX_Scanner/threatrule.l` | Valid and malformed extension feed scanned; scanner continues after invalid host/character | `Output_Files/design_challenge_tokens.txt`; `Output_Files/invalid_feed_errors.txt` | VERIFIED |
| Task 12D | Compare recognition, errors, time, tokens | `scripts/benchmark.py` | Five runs per mode, actual counters | Performance CSV/report | PARTIALLY VERIFIED |
| Report | Editable academic report and blank fields | `Assignment_Document/Assignment_1_Report.md`; `Cover_Page.md` | Content generated and evidence linked | Assignment document folder | PARTIALLY VERIFIED |
| Diagrams | Original system/phase/transition/testing diagrams | `scripts/generate_diagrams.py` | SVGs generated from source script | `Diagrams/` | VERIFIED |
| Viva | At least 25 Q&As | `Viva_Questions/Viva_Questions_and_Answers.md` | 34 entries supplied | Viva file | VERIFIED |
| Full compiler | Parser, complete semantic analysis, IR optimizer, target generator | Not implemented | Not tested | Report identifies boundary | NOT IMPLEMENTED |
| Submission images | Execution screenshots | Not supplied | Not tested | None | NOT TESTED |
