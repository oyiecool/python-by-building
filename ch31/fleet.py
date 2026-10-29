"""fleet.py - Chapter 31 mini project: run the health playbook from Python and report per host.

Usage:  python fleet.py                 # all hosts
        python fleet.py --limit web --check --min-free 25
"""
import argparse
import csv
import shutil
import sys
from datetime import datetime
from pathlib import Path

import ansible_runner

HERE = Path(__file__).resolve().parent


def run_playbook(limit=None, check=False, extravars=None):
    # ansible-runner saves cmdline and extravars under .runner/env and REUSES them on the
    # next call; clear them so a --check run cannot silently turn later runs into dry runs.
    shutil.rmtree(HERE / ".runner" / "env", ignore_errors=True)
    (HERE / ".runner").mkdir(exist_ok=True)
    r = ansible_runner.run(
        private_data_dir=str(HERE / ".runner"),       # runner keeps artifacts and logs here
        playbook=str(HERE / "site.yml"),
        inventory=str(HERE / "inventory.py"),         # the dynamic inventory script
        limit=limit,
        extravars=extravars or {},
        cmdline="--check --diff" if check else None,
        quiet=True,
    )
    return r


def collect(r) -> dict[str, dict]:
    hosts: dict[str, dict] = {}
    for e in r.events:
        if e["event"] not in ("runner_on_ok", "runner_on_failed", "runner_on_unreachable"):
            continue
        d = e["event_data"]
        h = hosts.setdefault(d["host"], {"host": d["host"], "status": "ok", "free_pct": "",
                                          "banner": "", "message": ""})
        res = d.get("res", {})
        if e["event"] == "runner_on_unreachable":
            h.update(status="UNREACHABLE", message=res.get("msg", ""))
        elif e["event"] == "runner_on_failed":
            h.update(status="FAILED", message=res.get("msg", ""))
        if "free_pct" in res:
            h["free_pct"] = res["free_pct"]
        if d["task"].startswith("Make sure the login banner"):
            h["banner"] = "changed" if res.get("changed") else "ok"
    return hosts


def main():
    ap = argparse.ArgumentParser(description="Fleet health check via Ansible")
    ap.add_argument("--limit", help="host or group pattern, e.g. web or db01")
    ap.add_argument("--check", action="store_true", help="dry run: report what would change")
    ap.add_argument("--min-free", type=int, default=15, help="minimum free disk space in percent")
    ap.add_argument("--motd", help="banner file to manage (default /etc/motd)")
    a = ap.parse_args()

    extra = {"min_free_pct": a.min_free}
    if a.motd:
        extra["motd_path"] = a.motd
    r = run_playbook(a.limit, a.check, extra)
    hosts = collect(r)

    out = HERE / f"fleet_report_{datetime.now():%Y%m%d_%H%M%S}.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["host", "status", "free_pct", "banner", "message"])
        w.writeheader()
        w.writerows(sorted(hosts.values(), key=lambda h: h["host"]))

    print(f"{'HOST':<9}{'STATUS':<13}{'FREE %':>7}  BANNER")
    for h in sorted(hosts.values(), key=lambda h: h["host"]):
        print(f"{h['host']:<9}{h['status']:<13}{h['free_pct']!s:>7}  {h['banner'] or '-'}  {h['message']}")
    st = r.stats or {}
    print(f"\n{len(hosts)} hosts, changed on {len(st.get('changed', {}))}, "
          f"failed on {len(st.get('failures', {}))}, unreachable {len(st.get('dark', {}))}"
          f"{' (check mode)' if a.check else ''}. Report: {out.name}")
    sys.exit(0 if r.rc == 0 else 2)


if __name__ == "__main__":
    main()
