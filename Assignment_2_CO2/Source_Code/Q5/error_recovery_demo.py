from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTS = {
    'catalogue': ROOT / 'Output_Files' / 'Q5_error_catalogue.txt',
    'panic': ROOT / 'Output_Files' / 'Q5_panic_mode.txt',
    'phrase': ROOT / 'Output_Files' / 'Q5_phrase_level.txt',
    'prod': ROOT / 'Output_Files' / 'Q5_error_productions.txt',
}

catalogue = '''Q5: Six-error catalogue with detection points
==============================================

1. Missing operand after operator
   Example: id + * id
   Detection point: after +, parser expects operand; * cannot begin operand.

2. Missing operator between operands
   Example: id id
   Detection point: after first id, expected operator or end-of-expression.

3. Unbalanced parentheses
   Example: (id + id
   Detection point: end of input while parser is still within parenthesized expression.

4. Dangling else
   Example: if E then if E then a else a
   Detection point: lookahead else when parser choice is ambiguous.

5. Invalid token sequence
   Example: id $ id
   Detection point: token $ is not valid in expression grammar.

6. Premature end of statement
   Example: id +
   Detection point: parser reaches end of input without operand.

LL and LR detection points:
- LL(1): blank table entry at lookahead symbol.
- LR: shift/reduce or reduce/reduce conflict or no valid action at current state.
'''

panic = '''Q5: Panic-mode recovery trace
==============================

Input: id + * id
Stack                            Input              Action
$E                               id + * id$         parse id
$E +                             * id$              panic: discard *
$E + id                          id$               recover and continue
$E                               $                 accept

Synchronizing tokens: +, ), $, and id after recovery.
This strategy prevents cascading errors by skipping invalid tokens until a safe point.
'''

phrase = '''Q5: Phrase-level recovery
=========================

Original input: id + * id
Recovery strategy: insert missing operand before *
Repaired string: id + id * id

The recovery is phrase-level because a missing operand is inserted locally without discarding useful input.
This keeps the parse tree meaningful and avoids unnecessary rollback.
'''

prod = '''Q5: Error productions
======================

Example grammar fragments:
E -> E + T | T
E -> E + error
T -> T * F | F
T -> error

Error productions allow the parser to continue after a lexical anomaly by replacing one bad phrase with error and resuming at a valid synchronizing token.

Message example: "operand expected before *"
Cascading messages are reduced because the parser resumes after a single, well-placed recovery point.
'''
for path in OUTS.values():
    path.parent.mkdir(parents=True, exist_ok=True)
OUTS['catalogue'].write_text(catalogue, encoding='utf-8')
OUTS['panic'].write_text(panic, encoding='utf-8')
OUTS['phrase'].write_text(phrase, encoding='utf-8')
OUTS['prod'].write_text(prod, encoding='utf-8')
print('Q5 outputs generated')
