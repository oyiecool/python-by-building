from pathlib import Path
import sys

text = Path(sys.argv[1]).read_text(encoding="utf-8")
print(f"{len(text.splitlines())} lines, {len(text.split())} words, {len(text)} characters")
