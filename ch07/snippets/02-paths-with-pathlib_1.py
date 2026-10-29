from pathlib import Path

here = Path.cwd()                         # current working directory
home = Path.home()                        # C:\Users\you or /home/you
reports = home / "Documents" / "reports"  # join with /
reports.mkdir(parents=True, exist_ok=True)

file = reports / "summary.txt"
file.write_text("All systems OK\n", encoding="utf-8")
print(file.read_text(encoding="utf-8"))

print(file.name, file.stem, file.suffix, file.parent)
print(file.exists(), file.is_file(), file.stat().st_size)

for p in reports.glob("*.txt"):           # rglob("*.txt") searches sub-folders
    print(p)
