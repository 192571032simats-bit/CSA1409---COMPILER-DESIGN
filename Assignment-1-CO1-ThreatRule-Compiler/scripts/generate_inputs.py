"""Generate deterministic ThreatRule benchmark inputs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIZES = (100, 1_000, 10_000, 100_000)
RULE = (
    'RULE ssh_attack IF src_ip == 10.0.0.5 AND port == 22 '
    'AND attempts > 5 THEN ALERT "SSH brute force" ;\n'
)


def main() -> None:
    inputs = ROOT / "Input_Files"
    inputs.mkdir(exist_ok=True)
    for size in SIZES:
        path = inputs / f"rules_{size}.tr"
        with path.open("w", encoding="ascii", newline="\n") as output:
            output.write(RULE * size)
        print(f"{path.relative_to(ROOT)}: {size} rules")


if __name__ == "__main__":
    main()
