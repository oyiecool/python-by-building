# syncbackup.py - Capstone 5
"""Incremental one-way backup: copy only new or changed files, verify with SHA-256,
keep deleted and replaced files in a dated archive instead of losing them."""
import argparse
import hashlib
import json
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

MANIFEST = ".backup_manifest.json"
ARCHIVE = ".archive"
SKIP = {".git", "__pycache__", ".venv", "node_modules", ARCHIVE}


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def scan(root: Path) -> dict[str, dict]:
    """Relative path -> size and modification time for every file under root."""
    files = {}
    for p in root.rglob("*"):
        if p.is_file() and not SKIP.intersection(p.relative_to(root).parts) and p.name != MANIFEST:
            st = p.stat()
            files[p.relative_to(root).as_posix()] = {"size": st.st_size, "mtime": int(st.st_mtime)}
    return files


def plan(src_files: dict, manifest: dict) -> tuple[list, list, list]:
    new = [f for f in src_files if f not in manifest]
    changed = [f for f in src_files if f in manifest and
               (src_files[f]["size"], src_files[f]["mtime"]) != (manifest[f]["size"], manifest[f]["mtime"])]
    deleted = [f for f in manifest if f not in src_files]
    return new, changed, deleted


def archive(dest: Path, rel: str, stamp: str) -> None:
    old = dest / rel
    if old.exists():
        target = dest / ARCHIVE / stamp / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old), target)


def run(src: Path, dest: Path, apply: bool) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    mpath = dest / MANIFEST
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    src_files = scan(src)
    new, changed, deleted = plan(src_files, manifest)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    logging.info("%d new, %d changed, %d deleted, %d unchanged",
                 len(new), len(changed), len(deleted), len(src_files) - len(new) - len(changed))
    if not apply:
        for label, items in (("NEW", new), ("CHANGED", changed), ("DELETED", deleted)):
            for f in items:
                print(f"  would {label.lower():<8} {f}")
        print("Dry run: nothing copied. Add --apply to run the backup.")
        return 0
    errors = 0
    for rel in new + changed:
        s, d = src / rel, dest / rel
        if rel in changed:
            archive(dest, rel, stamp)               # keep the previous version
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)                          # copy2 keeps the modification time
        digest = sha256(s)
        if sha256(d) != digest:
            logging.error("Verification failed for %s", rel)
            errors += 1
            continue
        manifest[rel] = {**src_files[rel], "sha256": digest}
        logging.info("copied %s", rel)
    for rel in deleted:
        archive(dest, rel, stamp)
        manifest.pop(rel, None)
        logging.info("archived deleted file %s", rel)
    mpath.write_text(json.dumps(manifest, indent=1, sort_keys=True))
    return errors


def verify(dest: Path) -> int:
    """Re-hash every backed-up file and compare with the manifest (detects bit rot)."""
    manifest = json.loads((dest / MANIFEST).read_text())
    bad = [rel for rel, info in manifest.items()
           if not (dest / rel).exists() or sha256(dest / rel) != info["sha256"]]
    for rel in bad:
        logging.error("CORRUPT OR MISSING: %s", rel)
    logging.info("Verified %d files, %d problems", len(manifest), len(bad))
    return len(bad)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Incremental backup with verification")
    ap.add_argument("source", type=Path)
    ap.add_argument("dest", type=Path)
    ap.add_argument("--apply", action="store_true", help="really copy (default is a dry run)")
    ap.add_argument("--verify", action="store_true", help="check the backup against its manifest")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler("syncbackup.log")])
    if not a.source.is_dir():
        sys.exit(f"Source {a.source} is not a folder")
    code = verify(a.dest) if a.verify else run(a.source.resolve(), a.dest.resolve(), a.apply)
    sys.exit(1 if code else 0)
