from pathlib import Path
import csv


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def write_lines(path, lines):
    ensure_dir(Path(path).parent)
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(str(line) + '\n')


def write_csv(path, rows):
    ensure_dir(Path(path).parent)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        if not rows:
            return
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
