from dataflow import reaching_definitions
from opt import optimize
from ir import Emitter


def verify():
    emitter = Emitter()
    emitter.emit("T1 = 2 + 3")
    emitter.emit("T2 = T1 * 4")
    emitter.emit("HALT")
    instructions = [str(instruction.index) + ": " + instruction.text for instruction in emitter.code]
    body = [instruction.split(": ", 1)[1] for instruction in instructions]

    optimized = optimize(body, 2)
    gen, definitions = reaching_definitions(body)
    assert "T1 = 5" in optimized
    assert "T2" in definitions
    print("Verification passed")
    print("Optimized:", optimized)


if __name__ == "__main__":
    verify()
