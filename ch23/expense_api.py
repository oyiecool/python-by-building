# expense_api.py - Chapter 23 mini project
"""A typed expense-tracking API with FastAPI, Pydantic validation and SQLite."""
import os
import sqlite3
from contextlib import contextmanager
from datetime import date
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

DB = os.environ.get("EXPENSE_DB", "expenses.db")
app = FastAPI(title="Expense API", version="1.0.0",
              description="Track spending by category. Interactive docs at /docs.")


class Category(str, Enum):
    food = "food"
    transport = "transport"
    utilities = "utilities"
    rent = "rent"
    health = "health"
    other = "other"


class ExpenseIn(BaseModel):
    spent_on: date = Field(default_factory=date.today, examples=["2026-10-29"])
    category: Category
    description: str = Field(min_length=1, max_length=120)
    amount: float = Field(gt=0, le=1_000_000, description="Amount in your currency")


class Expense(ExpenseIn):
    id: int


class Summary(BaseModel):
    month: str
    total: float
    by_category: dict[str, float]


def init_db() -> None:
    with sqlite3.connect(DB) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY, spent_on TEXT NOT NULL, category TEXT NOT NULL,
            description TEXT NOT NULL, amount REAL NOT NULL)""")


@contextmanager
def _connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def get_db():
    """A FastAPI dependency: each request gets its own connection, closed afterwards."""
    with _connect() as con:
        yield con


init_db()


@app.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(item: ExpenseIn, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
                     (item.spent_on.isoformat(), item.category.value, item.description, item.amount))
    return Expense(id=cur.lastrowid, **item.model_dump())


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: Category | None = None,
                  month: str | None = Query(None, pattern=r"^\d{4}-\d{2}$", examples=["2026-10"]),
                  limit: int = Query(50, ge=1, le=500),
                  db: sqlite3.Connection = Depends(get_db)):
    sql, args = "SELECT * FROM expenses WHERE 1=1", []
    if category:
        sql += " AND category = ?"
        args.append(category.value)
    if month:
        sql += " AND substr(spent_on, 1, 7) = ?"
        args.append(month)
    rows = db.execute(sql + " ORDER BY spent_on DESC, id DESC LIMIT ?", [*args, limit]).fetchall()
    return [dict(r) for r in rows]


@app.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"expense {expense_id} not found")
    return dict(row)


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: sqlite3.Connection = Depends(get_db)):
    if db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,)).rowcount == 0:
        raise HTTPException(status_code=404, detail=f"expense {expense_id} not found")


@app.get("/summary/{month}", response_model=Summary)
def summary(month: str, db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("SELECT category, SUM(amount) AS total FROM expenses "
                      "WHERE substr(spent_on, 1, 7) = ? GROUP BY category ORDER BY total DESC",
                      (month,)).fetchall()
    by_cat = {r["category"]: round(r["total"], 2) for r in rows}
    return Summary(month=month, total=round(sum(by_cat.values()), 2), by_category=by_cat)
