from datetime import datetime
from pathlib import Path

def largest_files(root: Path, n: int = 10):
    files = []
    for p in root.rglob("*"):
        try:
            if p.is_file():
                files.append((p.stat().st_size, p))
        except OSError:              # permission denied, broken links...
            continue
    return sorted(files, reverse=True)[:n]

def bulk_rename(folder: Path, apply: bool = False) -> None:
    """IMG_1234.jpeg -> 2026-09-21_221320.jpg, adding _1, _2 on collisions."""
    for p in sorted(folder.glob("*.jp*g")):
        stamp = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d_%H%M%S")
        target, n = p.with_name(f"{stamp}.jpg"), 1
        while target.exists() and target != p:
            target = p.with_name(f"{stamp}_{n}.jpg")
            n += 1
        if target == p:
            continue
        print(f"{'rename' if apply else 'would rename'} {p.name} -> {target.name}")
        if apply:
            p.rename(target)

for size, path in largest_files(Path.home()):
    print(f"{size / 2**20:8.1f} MB  {path}")
