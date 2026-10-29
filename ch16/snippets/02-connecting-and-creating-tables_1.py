import sqlite3

con = sqlite3.connect("shop.db")          # creates the file if missing
con.execute("PRAGMA foreign_keys = ON")   # enforce relationships
con.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    city  TEXT
);
CREATE TABLE IF NOT EXISTS orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    item        TEXT NOT NULL,
    amount      REAL NOT NULL CHECK (amount >= 0),
    ordered_at  TEXT DEFAULT (datetime('now'))
);
""")
