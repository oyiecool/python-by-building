"""vulncheck.py - Chapter 32 mini project: check Python dependencies against known vulnerabilities.

Data source: OSV.dev, the open vulnerability database used by pip-audit, GitHub and Google.
  python vulncheck.py requirements.txt                # online, asks api.osv.dev
  python vulncheck.py requirements.txt --db osv.json  # offline, a downloaded list of OSV records
  python vulncheck.py --installed                     # everything installed in this environment
"""
import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

OSV = "https://api.osv.dev/v1"
RANK = {"UNKNOWN": 0, "LOW": 1, "MODERATE": 2, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


@dataclass
class Finding:
    package: str
    version: str
    vuln_id: str
    cve: str
    severity: str
    fixed_in: str
    summary: str


# ---------- 1. what do we have? ----------
def read_requirements(path: Path) -> tuple[dict[str, str], list[str]]:
    pinned, skipped = {}, []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].split(";", 1)[0].strip()   # drop comments and markers
        if not line:
            continue
        m = re.fullmatch(r"([A-Za-z0-9._-]+)(\[[^\]]*\])?\s*==\s*(\S+)", line)
        if m:
            pinned[canonicalize_name(m.group(1))] = m.group(3)
        else:
            skipped.append(line)            # ranges like >=2.0 cannot be checked exactly
    return pinned, skipped


def installed() -> dict[str, str]:
    return {canonicalize_name(d.metadata["Name"]): d.version for d in metadata.distributions()}


# ---------- 2. which advisories apply? ----------
def in_range(v: Version, events: list[dict]) -> bool:
    """Walk OSV 'introduced'/'fixed'/'last_affected' events in order."""
    affected = False
    for ev in events:
        if "introduced" in ev:
            affected = affected or ev["introduced"] == "0" or v >= Version(ev["introduced"])
        elif "fixed" in ev and v >= Version(ev["fixed"]):
            affected = False
        elif "last_affected" in ev and v > Version(ev["last_affected"]):
            affected = False
    return affected


def affects(record: dict, name: str, version: str) -> tuple[bool, str]:
    v = Version(version)
    for aff in record.get("affected", []):
        pkg = aff.get("package", {})
        if pkg.get("ecosystem") != "PyPI" or canonicalize_name(pkg.get("name", "")) != name:
            continue
        if version in aff.get("versions", []):
            return True, ""
        for rng in aff.get("ranges", []):
            if rng.get("type") != "ECOSYSTEM":
                continue
            ev = rng["events"]
            if in_range(v, ev):
                fixes = sorted(Version(e["fixed"]) for e in ev if "fixed" in e and Version(e["fixed"]) > v)
                return True, str(fixes[0]) if fixes else "none yet"
    return False, ""


def severity(record: dict) -> str:
    s = (record.get("database_specific") or {}).get("severity", "UNKNOWN").upper()
    return s if s in RANK else "UNKNOWN"


def records_offline(db: Path) -> list[dict]:
    return json.loads(db.read_text(encoding="utf-8"))


def records_online(pkgs: dict[str, str], session=None) -> list[dict]:
    import requests                                    # only needed in online mode
    s = session or requests.Session()
    names = list(pkgs)
    body = {"queries": [{"package": {"name": n, "ecosystem": "PyPI"}, "version": pkgs[n]} for n in names]}
    r = s.post(f"{OSV}/querybatch", json=body, timeout=30)
    r.raise_for_status()
    ids = {v["id"] for res in r.json()["results"] for v in res.get("vulns", [])}
    out = []
    for vid in sorted(ids):                            # the batch answer has ids only: fetch details
        d = s.get(f"{OSV}/vulns/{vid}", timeout=30)
        d.raise_for_status()
        out.append(d.json())
    return out


def check(pkgs: dict[str, str], records: list[dict]) -> list[Finding]:
    found = []
    for name, ver in sorted(pkgs.items()):
        try:
            Version(ver)
        except InvalidVersion:
            continue
        for rec in records:
            hit, fix = affects(rec, name, ver)
            if hit:
                cve = next((a for a in rec.get("aliases", []) if a.startswith("CVE-")), "")
                found.append(Finding(name, ver, rec["id"], cve, severity(rec), fix, rec.get("summary", "")))
    return sorted(found, key=lambda f: (-RANK[f.severity], f.package))


# ---------- 3. report ----------
def main():
    ap = argparse.ArgumentParser(description="Check Python packages against OSV advisories")
    ap.add_argument("requirements", nargs="?", type=Path)
    ap.add_argument("--installed", action="store_true", help="check this environment instead")
    ap.add_argument("--db", type=Path, help="offline JSON list of OSV records")
    ap.add_argument("--csv", type=Path, help="also write the findings to a CSV file")
    ap.add_argument("--fail-on", default="HIGH", choices=["LOW", "MODERATE", "HIGH", "CRITICAL"])
    a = ap.parse_args()
    if not (a.requirements or a.installed):
        ap.error("give a requirements file or --installed")

    pkgs, skipped = (installed(), []) if a.installed else read_requirements(a.requirements)
    records = records_offline(a.db) if a.db else records_online(pkgs)
    findings = check(pkgs, records)

    for line in skipped:
        print(f"warning: not pinned, skipped: {line}")
    print(f"Checked {len(pkgs)} packages against {'offline' if a.db else 'live'} OSV data\n")
    for f in findings:
        print(f"[{f.severity:<8}] {f.package} {f.version}  {f.vuln_id} {f.cve}\n"
              f"            {f.summary}\n            fix: upgrade to {f.fixed_in}")
    vulnerable = {f.package for f in findings}
    print(f"\n{len(findings)} advisories in {len(vulnerable)} of {len(pkgs)} packages")
    if findings:
        upgrades = {}
        for f in findings:                             # highest fixed version per package wins
            if f.fixed_in not in ("", "none yet"):
                upgrades[f.package] = max(upgrades.get(f.package, f.fixed_in), f.fixed_in, key=Version)
        print("suggested pins: " + " ".join(f"{p}=={v}" for p, v in sorted(upgrades.items())))
    if a.csv:
        with a.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(Finding.__dataclass_fields__)
            w.writerows([list(vars(f).values()) for f in findings])
    worst = max((RANK[f.severity] for f in findings), default=0)
    sys.exit(1 if worst >= RANK[a.fail_on] else 0)


if __name__ == "__main__":
    main()
