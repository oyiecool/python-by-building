# backup.py - zip a folder with a timestamp, keep the newest N backups
import shutil, logging, sys
from datetime import datetime
from pathlib import Path

SOURCE = Path.home() / "Documents" / "important"
DEST = Path.home() / "Backups"
KEEP = 7

logging.basicConfig(filename=DEST / "backup.log" if DEST.exists() else None,
                    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def make_backup() -> Path:
    DEST.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive = shutil.make_archive(str(DEST / f"{SOURCE.name}-{stamp}"), "zip", SOURCE)
    return Path(archive)

def rotate():
    backups = sorted(DEST.glob(f"{SOURCE.name}-*.zip"))
    for old in backups[:-KEEP]:
        old.unlink()
        logging.info("Removed old backup %s", old.name)

if __name__ == "__main__":
    try:
        a = make_backup()
        logging.info("Created %s (%.1f MB)", a.name, a.stat().st_size / 1e6)
        rotate()
    except Exception:
        logging.exception("Backup failed")
        sys.exit(1)
