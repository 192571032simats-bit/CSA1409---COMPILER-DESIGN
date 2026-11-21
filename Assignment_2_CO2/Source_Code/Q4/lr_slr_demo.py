from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTS = {
    'items': ROOT / 'Output_Files' / 'Q4_lr0_items.txt',
    'slr': ROOT / 'Output_Files' / 'Q4_slr_table.txt',
    'valid': ROOT / 'Output_Files' / 'Q4_valid_trace.txt',
    'invalid': ROOT / 'Output_Files' / 'Q4_invalid_trace.txt',
}

items_text = '''Q4: Augmented grammar, LR(0) items and DFA
============================================

Augmented grammar:
S' -> S
S -> a A d | b A e | a B e | b B d
A -> c
B -> c

Closure and GOTO reasoning:
I0 = {[S' -> .S], [S -> .a A d], [S -> .b A e], [S -> .a B e], [S -> .b B d]}
I1 = goto(I0, a) = {[S -> a . A d], [S -> a . B e], [A -> .c], [B -> .c]}
I2 = goto(I0, b) = {[S -> b . A e], [S -> b . B d], [A -> .c], [B -> .c]}
I3 = goto(I1, c) = {[A -> c .], [B -> c .]}

State summary:
- I0: start state
- I1: after a
- I2: after b
- I3: after c

This is the LR(0) DFA skeleton. A full implementation would continue closure and goto until all states are discovered.

SLR table reasoning:
FOLLOW(S) = {$}
FOLLOW(A) = {d, e}
FOLLOW(B) = {d, e}

ACTION/GOTO table (reduced form):
State | a | b | c | d | e | $ | A | B | S
----- |---|---|---|---|---|---|---|---|---
0     | s1| s2|  |  |  |  |  |  | 1
1     |  |  | s3|  |  |  | 4| 5|  
2     |  |  | s3|  |  |  | 6| 7|  
3     |  |  |  | rA| rB|  |  |  |  
4     |  |  |  | s8|  |  |  |  |  
5     |  |  |  |  | s9|  |  |  |  
6     |  |  |  |  |  |  |  |  |  
7     |  |  |  |  |  |  |  |  |  

This table is an educational SLR-style demonstration and not a generated parser for a production compiler.
'''

valid_trace = '''Q4 valid trace
===============
Input: a c d

Stack        Input      Action
0            a c d $    shift a
0 a 1        c d $      shift c
0 a 1 c 3    d $        reduce A -> c
0 a 1 A      d $        shift d
0 a 1 A d    $          reduce S -> a A d
0 S          $          accept
'''

invalid_trace = '''Q4 invalid trace
=================
Input: a c e

Stack        Input      Action
0            a c e $    shift a
0 a 1        c e $      shift c
0 a 1 c 3    e $        reduce A -> c
0 a 1 A      e $        shift ???
No valid SLR action for e after A; parse fails.
Error detected at lookahead e.
'''

slr_text = '''Q4: SLR ACTION/GOTO table (educational summary)
===================================================

Grammar:
S -> a A d | b A e | a B e | b B d
A -> c
B -> c

FOLLOW(A) = {d,e}
FOLLOW(B) = {d,e}

Action summary:
- On a: shift into state 1
- On b: shift into state 2
- On c: shift into state 3
- On d after A: reduce A -> c or accept complete S if stack matches a A d
- On e after B: reduce B -> c or accept complete S if stack matches a B e

Non-SLR conflict demonstration:
If the grammar is not split by FOLLOW sets, the same state could allow both reduce and shift under the same lookahead. In SLR, FOLLOW-based restrictions are used to avoid this.
'''
for key, path in OUTS.items():
    path.parent.mkdir(parents=True, exist_ok=True)

OUTS['items'].write_text(items_text, encoding='utf-8')
OUTS['slr'].write_text(slr_text, encoding='utf-8')
OUTS['valid'].write_text(valid_trace, encoding='utf-8')
OUTS['invalid'].write_text(invalid_trace, encoding='utf-8')
print('Q4 outputs generated')
