# expenses.py
import csv
from datetime import date
from pathlib import Path
from collections import defaultdict

DATA = Path(__file__).resolve().parent / "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]

def load():
    if not DATA.exists():
        return []
    with DATA.open(newline="", encoding="utf-8") as f:
        return [{**r, "amount": float(r["amount"])} for r in csv.DictReader(f)]

def save(rows):
    with DATA.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

def add(rows):
    rows.append({
        "date": input(f"Date [{date.today()}]: ") or str(date.today()),
        "category": input("Category: ").strip().title(),
        "description": input("Description: ").strip(),
        "amount": float(input("Amount: ")),
    })
    save(rows)

def summary(rows):
    by_month = defaultdict(lambda: defaultdict(float))
    for r in rows:
        by_month[r["date"][:7]][r["category"]] += r["amount"]
    for month in sorted(by_month):
        cats = by_month[month]
        print(f"\n{month}  total {sum(cats.values()):,.2f}")
        for cat, amt in sorted(cats.items(), key=lambda kv: -kv[1]):
            share = amt / sum(cats.values())
            print(f"  {cat:<14}{amt:>10,.2f}  {share:>5.0%}  {'#' * round(share * 30)}")

if __name__ == "__main__":
    rows = load()
    while True:
        c = input("\n[a]dd  [l]ist  [s]ummary  [q]uit: ").lower()
        if c == "a":
            add(rows)
        elif c == "l":
            for r in rows[-10:]:
                print(f"{r['date']}  {r['category']:<12}{r['amount']:>10,.2f}  {r['description']}")
        elif c == "s":
            summary(rows)
        elif c == "q":
            break
