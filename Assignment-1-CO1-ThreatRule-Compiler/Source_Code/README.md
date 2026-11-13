# Source-code scope

The compiled C scanner is generated from
[`../LEX_Scanner/threatrule.l`](../LEX_Scanner/threatrule.l) into
[`../LEX_Scanner/lex.yy.c`](../LEX_Scanner/lex.yy.c). Keeping the source of
truth in the LEX specification avoids maintaining a second hand-written lexer.

No separate parser, semantic-analysis, intermediate-code, optimizer, or
target-code C modules are supplied: those stages are explicitly not implemented
in this lexical-analyzer project. Their conceptual roles and illustrative
outputs are documented in the assignment report; they should not be mistaken
for runnable compiler components.
