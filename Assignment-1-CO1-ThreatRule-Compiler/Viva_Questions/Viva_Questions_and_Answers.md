# Viva Questions and Answers

1. **What does a compiler do?** It translates a source program into another representation or target program, usually while reporting errors.
2. **How is an interpreter different?** It executes source or an intermediate representation directly rather than first producing a standalone target program.
3. **What is an assembler?** A translator from assembly mnemonics to machine/object code.
4. **What is a hybrid compiler?** A compiler that emits intermediate code/bytecode executed or further compiled by a virtual machine.
5. **What is a token?** A lexical category such as `IDENTIFIER` or `IPV4`.
6. **What is a lexeme?** The concrete source substring matched for a token, such as `ssh_attack`.
7. **What is a token pattern?** A rule describing all strings belonging to a token class.
8. **What is a regular expression?** A notation for specifying a regular language.
9. **What is a finite automaton?** A state machine that recognizes regular languages by consuming input symbols.
10. **What does LEX/Flex generate?** C source implementing a scanner from regular-expression/action rules.
11. **What is `yytext`?** Flex's pointer to the current matched lexeme.
12. **What does `yyleng` contain?** The length of that current lexeme.
13. **What is `yylineno` used for here?** Reporting the source line associated with a token or diagnostic.
14. **What is `yylval`?** A parser/lexer semantic-value object used to pass token attributes to a parser; this standalone scanner does not use it.
15. **What is a symbol table?** A mapping of names to their attributes; this prototype stores distinct identifier spellings.
16. **What is maximal munch?** Selecting the longest input prefix matching any token rule.
17. **How are equal-length Flex matches resolved?** The rule appearing first wins.
18. **How does `<` differ from `<=`?** Look ahead one character; consume `=` if present, otherwise retract it and accept `<`.
19. **Why remove whitespace in the scanner?** It usually separates tokens but is not needed by later syntax analysis.
20. **How are comments handled?** Recognized comment patterns are consumed and discarded while line counting continues.
21. **What is lexical error recovery?** Report a bad lexeme, consume enough input to make progress, then resume tokenization.
22. **How is the IPv4 boundary checked?** Parse four decimal octets and require each value to be 0–255.
23. **What port range is accepted?** 0–65535, inclusive, when a value follows the `port` field.
24. **What is input buffering?** Reading blocks of characters to avoid an input operation for every character; classic scanners can use paired buffers and sentinels.
25. **What is a compiler pass?** One traversal or analysis over a source/intermediate representation.
26. **Why use a multi-pass design?** It separates concerns and supports clearer diagnostics and transformations, though it may cost extra time/memory.
27. **What is the front end?** The source-language-dependent scanning, parsing, and semantic-analysis portion.
28. **What is the back end?** Target-oriented optimization and code generation consuming an IR.
29. **How are hashes recognized in the extension?** Hexadecimal strings of exactly 32, 40, or 64 characters are accepted as MD5/SHA-1/SHA-256-shaped lexemes.
30. **What CVE syntax is supported?** `CVE-`, at least four year digits, a hyphen, and at least one identifier digit.
31. **What URL syntax is supported?** Lowercase HTTP/HTTPS, an ASCII hostname, and optional path/query/fragment without whitespace or specified delimiters.
32. **How was performance measured?** Five fresh scanner runs per file, with median wall-clock process time and token/error counts from the scanner.
33. **Does 100,000-rule scanning prove production readiness?** No; it demonstrates this scanner's test-input handling, not parser, policy, throughput, or deployment readiness.
34. **What is the most important limitation?** The project does not implement a grammar parser or later compiler phases; AST/IR/target examples are illustrative.
