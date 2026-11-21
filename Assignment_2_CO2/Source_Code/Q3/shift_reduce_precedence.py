from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT1 = ROOT / 'Output_Files' / 'Q3_shift_reduce.txt'
OUT2 = ROOT / 'Output_Files' / 'Q3_operator_precedence.txt'

content1 = '''Q3: Hand-derived reductions and shift-reduce parsing
=====================================================

Expression: id + id * id
Grammar:
E -> E + T | T
T -> T * F | F
F -> id

Handle detection:
1. id -> F -> T -> E (after reading first id)
2. + is next, so reduce id to F and then to T and then E before shifting +
3. Then read id, reduce again, then shift *
4. When * follows E + id, shift because * has higher precedence than +
5. Final reduction yields E -> E + T -> E + T * F -> E + T -> E

Shift-reduce trace:
Stack                Input                     Action
$                    id + id * id$            shift
$id                  + id * id$               reduce F -> id
$F                   + id * id$               reduce T -> F
$T                   + id * id$               reduce E -> T
$E +                 id * id$                 shift
$E + id              * id$                    reduce F -> id
$E + F               * id$                    reduce T -> F
$E + T               * id$                    shift
$E + T *             id$                     shift
$E + T * id          $                       reduce F -> id
$E + T * F           $                       reduce T -> T * F
$E + T               $                       reduce E -> E + T
$E                   $                       ACCEPT

Conflict examples:
- shift/reduce conflict: when parsing E + E * E, grammar may either reduce + or shift *.
- reduce/reduce conflict: grammar with E -> A | B and A/B both reduce same prefix can create ambiguity.

Conclusion:
The parser resolves the conflict by precedence and associativity rules.
'''

content2 = '''Q3: Operator-precedence relation table
=======================================

For operators +, *, and parentheses:

Operator     Relation            Explanation
-----------------------------------------------------
(            less-than           opening parenthesis has highest precedence
*            greater-than        * has higher precedence than +
+            less-than           + binds weaker than *
)            greater-than        closing parenthesis ends grouped expression

Complete precedence table:

    +    *    (    )    id
+   <    >    <    >    <
*   >    >    <    >    <
(   <    <    <    =    <
)   >    >    >    >    error
id  >    >    error  >    error

Two precedence-based parses:
1. id + id * id => id + (id * id)
2. id * id + id => (id * id) + id

The precedence relation table determines whether to shift or reduce at each operator.
'''
OUT1.parent.mkdir(parents=True, exist_ok=True)
OUT1.write_text(content1, encoding='utf-8')
OUT2.write_text(content2, encoding='utf-8')
print('Q3 outputs generated')
