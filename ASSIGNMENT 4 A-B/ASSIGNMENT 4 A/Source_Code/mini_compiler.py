import argparse
import re
from pathlib import Path

from symtab import SymbolTable
from ir import Emitter
from expr import ExprGenerator
from backpatch import BooleanGenerator


class MiniCompiler:
    def __init__(self):
        self.symbols = SymbolTable()
        self.emitter = Emitter()
        self.expr = ExprGenerator(self.symbols, self.emitter)
        self.boolean = BooleanGenerator(self.emitter)

    def declarations(self, source):
        for typ, names in re.findall(r"(int|float|boolean)\s+([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*;", source):
            for name in names.split(","):
                self.symbols.declare(name.strip(), typ)

    def compile(self, source):
        self.declarations(source)
        assignment_pattern = re.compile(r"([A-Za-z_]\w*)\s*=\s*([^;]+);")
        for name, expression in assignment_pattern.findall(source):
            expression = expression.strip()
            if re.fullmatch(r"-?\d+(?:\.\d+)?", expression):
                typ = "float" if "." in expression else "int"
                place = expression
            else:
                operands = re.split(r"\s*([+\-*/])\s*", expression)
                if len(operands) == 3:
                    left = operands[0]
                    op = operands[1]
                    right = operands[2]
                    left_place, left_type = self.expr.identifier(left) if re.match(r"^[A-Za-z_]\w*$", left) else (left, "float" if "." in left else "int")
                    right_place, right_type = self.expr.identifier(right) if re.match(r"^[A-Za-z_]\w*$", right) else (right, "float" if "." in right else "int")
                    place, typ = self.expr.binary(op, left_place, left_type, right_place, right_type)
                elif re.match(r"^[A-Za-z_]\w*$", expression):
                    place, typ = self.expr.identifier(expression)
                else:
                    raise ValueError(f"unsupported expression '{expression}'")
            self.expr.assign(name, place, typ)
        self.emitter.emit_halt()
        return self.emitter.code

    def format(self):
        return "\n".join(str(instruction) for instruction in self.emitter.code)


def main():
    parser = argparse.ArgumentParser(description="Assignment 4A mini compiler")
    parser.add_argument("input", nargs="?", help="Input source file")
    args = parser.parse_args()
    source = Path(args.input).read_text(encoding="utf-8") if args.input else "int a, b; float c; a = b + 2; c = a * 3;"
    compiler = MiniCompiler()
    compiler.compile(source)
    print(compiler.format())


if __name__ == "__main__":
    main()
