import argparse, shutil
from pathlib import Path

TYPES = {"Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
         "Documents": {".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".csv"},
         "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
         "Audio": {".mp3", ".wav", ".m4a"}, "Video": {".mp4", ".mkv", ".mov"}}

def folder_for(path: Path) -> str:
    ext = path.suffix.lower()
    return next((name for name, exts in TYPES.items() if ext in exts), "Other")

ap = argparse.ArgumentParser()
ap.add_argument("folder", type=Path)
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()
for f in sorted(a.folder.iterdir()):
    if f.is_file():
        target = a.folder / folder_for(f) / f.name
        print(("move " if a.apply else "would move ") + f"{f.name} -> {target.parent.name}/")
        if a.apply:
            target.parent.mkdir(exist_ok=True)
            shutil.move(str(f), target)
