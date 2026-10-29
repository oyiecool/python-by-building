# inventory_client.py - Capstone 8 client
"""Bulk-load assets from CSV into the API and print a report, using requests."""
import csv
import os
import sys

import requests

API = os.environ.get("INVENTORY_URL", "http://127.0.0.1:5001/api")
KEY = os.environ.get("INVENTORY_API_KEY", "dev-key-change-me")
session = requests.Session()
session.headers.update({"X-API-Key": KEY})

SAMPLE = """tag,name,category,owner,location,cost
LT-001,ThinkPad T14 Gen 4,laptop,ana,Manila,65000
LT-002,MacBook Air M3,laptop,ben,Cebu,72000
SV-001,Dell PowerEdge R650,server,,Data center,420000
NW-001,Cisco Catalyst 9200,network,,Data center,180000
PR-001,HP LaserJet M507,printer,,Manila 3F,38000
LC-001,Microsoft 365 E3 (50 seats),license,it,Cloud,1150000
"""


def load_csv(text: str) -> None:
    for row in csv.DictReader(text.splitlines()):
        row = {k: v for k, v in row.items() if v}            # drop empty fields
        r = session.post(f"{API}/assets", json=row, timeout=10)
        if r.status_code == 201:
            print(f"  added   {row['tag']}")
        elif r.status_code == 409:
            print(f"  exists  {row['tag']}")
        else:
            print(f"  FAILED  {row['tag']}: {r.json().get('message')}")


def report() -> None:
    stats = session.get(f"{API}/stats", timeout=10).json()
    total = sum(s["total_cost"] for s in stats)
    print(f"\n{'Category':<10}{'Count':>6}{'Total cost':>16}{'Share':>8}")
    for s in stats:
        print(f"{s['category']:<10}{s['count']:>6}{s['total_cost']:>16,.2f}{s['total_cost'] / total:>8.0%}")
    laptops = session.get(f"{API}/assets", params={"category": "laptop"}, timeout=10).json()
    print("\nLaptops and owners:", ", ".join(f"{a['tag']}={a['owner'] or '?'}" for a in laptops))


if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else SAMPLE
    try:
        load_csv(text)
        report()
    except requests.ConnectionError:
        sys.exit("API not running: start it with  python inventory_api.py")
