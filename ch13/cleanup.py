# cleanup.py - delete files older than N days in a folder
import argparse, logging, time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def old_files(folder: Path, days: int, pattern: str):
    cutoff = time.time() - days * 86400
    for p in folder.rglob(pattern):
        if p.is_file() and p.stat().st_mtime < cutoff:
            yield p

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--pattern", default="*.log")
    ap.add_argument("--delete", action="store_true", help="actually delete (default: dry run)")
    a = ap.parse_args()
    freed = count = 0
    for f in old_files(a.folder, a.days, a.pattern):
        size = f.stat().st_size
        if a.delete:
            f.unlink()
        logging.info("%s %s (%.1f KB)", "Deleted" if a.delete else "Would delete", f, size / 1024)
        freed += size; count += 1
    logging.info("%d files, %.1f MB %s", count, freed / 1e6, "freed" if a.delete else "reclaimable")
