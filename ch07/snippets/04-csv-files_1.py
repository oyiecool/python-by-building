import csv

rows = [
    {"date": "2026-10-01", "category": "Food", "amount": 350.0},
    {"date": "2026-10-02", "category": "Transport", "amount": 120.0},
]

with open("expenses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "category", "amount"])
    writer.writeheader()
    writer.writerows(rows)

with open("expenses.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["category"], float(row["amount"]))   # values arrive as strings
