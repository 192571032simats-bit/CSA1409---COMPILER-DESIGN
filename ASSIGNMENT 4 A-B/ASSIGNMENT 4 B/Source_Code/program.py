import argparse

from codegen import CodeGenerator


def main():
    parser = argparse.ArgumentParser(description="Assignment 4B kernel intermediate-code generator")
    parser.add_argument("--step", default="1", help="Loop STEP expression")
    args = parser.parse_args()

    generator = CodeGenerator()
    a = generator.expression("i", "+", "1")
    b = generator.expression("i", "*", "2")
    generator.array_store("A", "i", "j", "10", b)
    loaded = generator.array_load("A", "i", "j", "10")
    generator.expression(loaded, "+", "1")
    generator.emitter.finish()

    print(f"STEP={args.step}")
    for instruction in generator.emitter.code:
        print(instruction)


if __name__ == "__main__":
    main()
