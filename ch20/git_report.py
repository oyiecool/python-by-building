# git_report.py - Chapter 20 mini project
"""Summarize a Git repository's history: activity per author, weekday and hour, busiest files."""
import argparse
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

SEP = "\x1f"     # a character that never appears in commit messages


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"git error: {result.stderr.strip()}")
    return result.stdout


def commits(repo: Path, since: str | None) -> list[dict]:
    fmt = SEP.join(["%H", "%an", "%aI", "%s"])
    args = ["log", f"--pretty=format:{fmt}", "--numstat"]
    if since:
        args.append(f"--since={since}")
    out, current = [], None
    for line in git(repo, *args).splitlines():
        if SEP in line:
            sha, author, when, subject = line.split(SEP)
            current = {"sha": sha[:7], "author": author, "when": datetime.fromisoformat(when),
                       "subject": subject, "added": 0, "deleted": 0, "files": []}
            out.append(current)
        elif line.strip() and current:
            added, deleted, path = line.split("\t")
            current["added"] += int(added) if added.isdigit() else 0      # "-" for binary files
            current["deleted"] += int(deleted) if deleted.isdigit() else 0
            current["files"].append(path)
    return out


def report(cs: list[dict]) -> None:
    if not cs:
        print("No commits in that range.")
        return
    first, last = min(c["when"] for c in cs), max(c["when"] for c in cs)
    print(f"{len(cs)} commits from {first:%Y-%m-%d} to {last:%Y-%m-%d}\n")
    authors = Counter(c["author"] for c in cs)
    lines = Counter()
    for c in cs:
        lines[c["author"]] += c["added"] + c["deleted"]
    print(f"{'Author':<20}{'Commits':>8}{'Lines changed':>15}")
    for a, n in authors.most_common():
        print(f"{a:<20}{n:>8}{lines[a]:>15,}")
    days = Counter(c["when"].strftime("%a") for c in cs)
    print("\nCommits by weekday:")
    for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        print(f"  {d} {'#' * days[d]} {days[d]}")
    hours = Counter(c["when"].hour for c in cs)
    print(f"\nBusiest hour: {hours.most_common(1)[0][0]:02d}:00")
    files = Counter(f for c in cs for f in c["files"])
    print("\nMost frequently changed files (refactoring candidates):")
    for f, n in files.most_common(5):
        print(f"  {n:>3}  {f}")
    fixes = sum("fix" in c["subject"].lower() for c in cs)
    print(f"\n{fixes} of {len(cs)} commits ({fixes / len(cs):.0%}) mention a fix.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Summarize a Git repository's history")
    ap.add_argument("repo", nargs="?", type=Path, default=Path("."))
    ap.add_argument("--since", help='e.g. "3 months ago" or 2026-01-01')
    a = ap.parse_args()
    report(commits(a.repo, a.since))
