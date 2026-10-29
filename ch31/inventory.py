#!/usr/bin/env python3
"""inventory.py - Ansible dynamic inventory built from a CMDB export (cmdb.csv).

Ansible runs this script with --list (whole inventory) or --host NAME (one host's variables)
and reads JSON from its standard output."""
import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path

CMDB = Path(os.environ.get("CMDB_CSV", Path(__file__).with_name("cmdb.csv")))


def build() -> dict:
    groups = defaultdict(lambda: {"hosts": []})
    hostvars = {}
    with CMDB.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["name"].strip()
            groups[row["group"]]["hosts"].append(name)
            groups[row["env"]]["hosts"].append(name)          # e.g. prod, dev
            hostvars[name] = {"ansible_host": row["address"], "env": row["env"]}
            if row.get("connection"):                          # "local" for the lab, empty for SSH
                hostvars[name]["ansible_connection"] = row["connection"]
    inv = dict(groups)
    inv["all"] = {"children": sorted(groups)}
    inv["_meta"] = {"hostvars": hostvars}                      # saves one --host call per host
    return inv


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--host")
    a = ap.parse_args()
    inv = build()
    print(json.dumps(inv["_meta"]["hostvars"].get(a.host, {}) if a.host else inv, indent=2))
