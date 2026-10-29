# helpdesk.py
import sqlite3
from datetime import datetime
from pathlib import Path

DB = Path(__file__).resolve().parent / "helpdesk.db"
STATUSES = ("open", "in progress", "resolved")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, department TEXT
);
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 3),
    status TEXT NOT NULL DEFAULT 'open',
    opened_at TEXT NOT NULL,
    closed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
"""

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)
    return con

def add_user(con, name, dept):
    with con:
        return con.execute("INSERT INTO users (name, department) VALUES (?, ?)", (name, dept)).lastrowid

def open_ticket(con, user_id, title, category, priority=2):
    with con:
        return con.execute(
            "INSERT INTO tickets (user_id, title, category, priority, opened_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, title, category, priority, datetime.now().isoformat(timespec="minutes"))).lastrowid

def set_status(con, ticket_id, status):
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    closed = datetime.now().isoformat(timespec="minutes") if status == "resolved" else None
    with con:
        n = con.execute("UPDATE tickets SET status = ?, closed_at = ? WHERE id = ?",
                        (status, closed, ticket_id)).rowcount
    if n == 0:
        raise LookupError(f"no ticket {ticket_id}")

def queue(con):
    return con.execute("""
        SELECT t.id, t.priority, t.status, t.title, u.name, u.department, t.opened_at
        FROM tickets t JOIN users u ON u.id = t.user_id
        WHERE t.status != 'resolved'
        ORDER BY t.priority, t.opened_at""").fetchall()

def report(con):
    return con.execute("""
        SELECT category,
               COUNT(*) AS total,
               SUM(status = 'resolved') AS resolved,
               ROUND(AVG(CASE WHEN closed_at IS NOT NULL
                     THEN (julianday(closed_at) - julianday(opened_at)) * 24 END), 1) AS avg_hours
        FROM tickets GROUP BY category ORDER BY total DESC""").fetchall()

if __name__ == "__main__":
    con = connect()
    if not con.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        ana = add_user(con, "Ana Cruz", "Finance")
        ben = add_user(con, "Ben Santos", "Sales")
        t1 = open_ticket(con, ana, "Cannot print to 3F printer", "Hardware", 2)
        open_ticket(con, ben, "VPN disconnects every hour", "Network", 1)
        open_ticket(con, ana, "Need Excel license", "Software", 3)
        set_status(con, t1, "resolved")
    print("OPEN QUEUE")
    for r in queue(con):
        print(f"#{r['id']:<4}P{r['priority']}  {r['status']:<12}{r['title']:<32}{r['name']} ({r['department']})")
    print("\nBY CATEGORY")
    for r in report(con):
        print(f"{r['category']:<10}{r['total']:>4} total {r['resolved']:>3} resolved  avg {r['avg_hours']} h")
