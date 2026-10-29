# price_tracker.py - Capstone 7
"""Track product prices over time in SQLite and alert when a price drops below your target."""
import argparse
import random
import re
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
DB = BASE / "prices.db"
HEADERS = {"User-Agent": "python-by-building-price-tracker/1.0 (learning project)"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY, url TEXT UNIQUE NOT NULL, title TEXT, target REAL
);
CREATE TABLE IF NOT EXISTS prices (
    product_id INTEGER NOT NULL REFERENCES products(id),
    checked_at TEXT NOT NULL, price REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_prices ON prices(product_id, checked_at);
"""


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def parse_price(text: str) -> float:
    """'£51.77', '₱1,299.00', '$ 45' -> 51.77, 1299.0, 45.0"""
    digits = re.sub(r"[^\d.]", "", text.replace(",", ""))
    if not digits:
        raise ValueError(f"no price in {text!r}")
    return float(digits)


def fetch(url: str) -> tuple[str, float]:
    """Download a product page and extract its title and price.
    Selectors match books.toscrape.com; adjust them for other sites (Chapter 14)."""
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    title = soup.select_one("div.product_main h1").get_text(strip=True)
    price = parse_price(soup.select_one("div.product_main p.price_color").get_text())
    return title, price


def add(con, url: str, target: float) -> None:
    title, price = fetch(url)
    with con:
        con.execute("INSERT OR REPLACE INTO products (url, title, target) VALUES (?, ?, ?)",
                    (url, title, target))
    print(f"Watching '{title}' (now {price:.2f}, target {target:.2f})")


def check(con, demo: bool = False) -> list[str]:
    alerts = []
    for p in con.execute("SELECT * FROM products").fetchall():
        try:
            if demo:
                last = con.execute("SELECT price FROM prices WHERE product_id=? ORDER BY checked_at DESC LIMIT 1",
                                   (p["id"],)).fetchone()
                price = round((last["price"] if last else p["target"] * 1.25) * random.uniform(0.94, 1.04), 2)
            else:
                _, price = fetch(p["url"])
                time.sleep(1)                       # be polite to the site
        except (requests.RequestException, AttributeError, ValueError) as e:
            print(f"  ! {p['title']}: {e}")
            continue
        prev = con.execute("SELECT price FROM prices WHERE product_id=? ORDER BY checked_at DESC LIMIT 1",
                           (p["id"],)).fetchone()
        with con:
            con.execute("INSERT INTO prices VALUES (?, ?, ?)",
                        (p["id"], datetime.now().isoformat(timespec="seconds"), price))
        change = f"{(price / prev['price'] - 1):+.1%}" if prev else "first check"
        print(f"  {p['title'][:40]:<42}{price:>9.2f}  {change}")
        if price <= p["target"]:
            alerts.append(f"{p['title']} is {price:.2f} (target {p['target']:.2f}) {p['url']}")
    return alerts


def history(con, out: Path) -> None:
    import matplotlib.pyplot as plt
    import pandas as pd
    df = pd.read_sql_query("SELECT p.title, p.target, h.checked_at, h.price FROM prices h "
                           "JOIN products p ON p.id = h.product_id ORDER BY h.checked_at",
                           con, parse_dates=["checked_at"])
    if df.empty:
        print("No price history yet.")
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    for title, g in df.groupby("title"):
        line, = ax.plot(g["checked_at"], g["price"], marker=".", label=title[:30])
        ax.axhline(g["target"].iloc[0], color=line.get_color(), linestyle=":", linewidth=1)
    ax.set(title="Price history (dotted = your target)", ylabel="Price")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    print(f"Chart saved to {out}")


def seed_demo(con) -> None:
    """Offline demo: three products and 30 days of simulated checks."""
    random.seed(4)
    items = [("Demo: The Pragmatic Programmer", 38.0), ("Demo: Clean Code", 30.0), ("Demo: Fluent Python", 45.0)]
    with con:
        for i, (title, target) in enumerate(items, start=1):
            con.execute("INSERT OR IGNORE INTO products (id, url, title, target) VALUES (?, ?, ?, ?)",
                        (i, f"https://example.com/demo/{i}", title, target))
            price = target * 1.3
            for d in range(30):
                price = round(price * random.uniform(0.95, 1.035), 2)
                t = (datetime.now() - timedelta(days=30 - d)).isoformat(timespec="seconds")
                con.execute("INSERT INTO prices VALUES (?, ?, ?)", (i, t, price))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Price tracker")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_add = sub.add_parser("add", help="watch a product URL")
    a_add.add_argument("url")
    a_add.add_argument("target", type=float)
    a_chk = sub.add_parser("check", help="check all prices now")
    a_chk.add_argument("--demo", action="store_true", help="simulate prices offline")
    sub.add_parser("chart", help="plot price history")
    sub.add_parser("demo", help="create offline demo data")
    args = ap.parse_args()
    con = connect()
    if args.cmd == "add":
        add(con, args.url, args.target)
    elif args.cmd == "check":
        print(f"Checking prices at {datetime.now():%Y-%m-%d %H:%M}")
        for alert in check(con, demo=args.demo):
            print("  PRICE ALERT:", alert)       # or send_alert() from Chapter 13
    elif args.cmd == "chart":
        history(con, BASE / "price_history.png")
    elif args.cmd == "demo":
        seed_demo(con)
        print("Demo data created. Try: check --demo, then chart")
