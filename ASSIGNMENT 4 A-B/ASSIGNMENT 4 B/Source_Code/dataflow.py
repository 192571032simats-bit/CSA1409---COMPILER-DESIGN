def basic_blocks(instructions):
    leaders = {0}
    for i, text in enumerate(instructions):
        if text.startswith("if ") or text.startswith("goto ") or text == "HALT":
            if i + 1 < len(instructions):
                leaders.add(i + 1)
    blocks = []
    starts = sorted(leaders)
    for i, start in enumerate(starts):
        end = (starts[i + 1] if i + 1 < len(starts) else len(instructions))
        blocks.append(list(range(start, end)))
    return blocks


def successors(block, instructions, blocks):
    first = block[0]
    last = block[-1]
    text = instructions[last]
    if text == "HALT":
        return []
    if text.startswith("goto "):
        return []
    return [blocks.index([b for b in blocks if b[0] == last + 1][0])] if last + 1 < len(instructions) else []


def reaching_definitions(instructions):
    definitions = {}
    gen = {}
    for i, text in enumerate(instructions):
        if " = " in text:
            name = text.split(" = ", 1)[0].strip()
            gen[i] = {name}
            definitions[name] = i
    return gen, definitions
