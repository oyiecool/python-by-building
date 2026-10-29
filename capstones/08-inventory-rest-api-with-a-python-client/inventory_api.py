# inventory_api.py - Capstone 8
"""A REST API for IT assets (laptops, servers, licences) backed by SQLite."""
import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, g, jsonify, request

DB = Path(os.environ.get("INVENTORY_DB", Path(__file__).resolve().parent / "inventory.db"))
API_KEY = os.environ.get("INVENTORY_API_KEY", "dev-key-change-me")
FIELDS = {"tag": str, "name": str, "category": str, "owner": str, "location": str, "cost": float}
CATEGORIES = {"laptop", "desktop", "server", "network", "printer", "license", "other"}

app = Flask(__name__)


def db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute("""CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY, tag TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
            category TEXT NOT NULL, owner TEXT DEFAULT '', location TEXT DEFAULT '',
            cost REAL DEFAULT 0, created_at TEXT DEFAULT (datetime('now')))""")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    if (con := g.pop("db", None)) is not None:
        con.close()


@app.before_request
def require_key():
    """Reads are open; changes need the X-API-Key header."""
    if request.method in ("POST", "PUT", "PATCH", "DELETE") and request.headers.get("X-API-Key") != API_KEY:
        abort(401, description="missing or wrong X-API-Key")


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(409)
def json_error(e):
    return jsonify(error=e.name, message=e.description), e.code


def validate(data: dict, partial: bool = False) -> dict:
    clean = {}
    for field, typ in FIELDS.items():
        if field in data:
            try:
                clean[field] = typ(data[field])
            except (TypeError, ValueError):
                abort(400, description=f"{field} must be {typ.__name__}")
        elif not partial and field in ("tag", "name", "category"):
            abort(400, description=f"{field} is required")
    if "category" in clean and clean["category"] not in CATEGORIES:
        abort(400, description=f"category must be one of {sorted(CATEGORIES)}")
    if clean.get("cost", 0) < 0:
        abort(400, description="cost cannot be negative")
    return clean


@app.get("/api/assets")
def list_assets():
    sql, args = "SELECT * FROM assets WHERE 1=1", []
    for field in ("category", "owner", "location"):
        if value := request.args.get(field):
            sql += f" AND {field} = ?"               # field comes from our fixed tuple, value is a parameter
            args.append(value)
    if q := request.args.get("q"):
        sql += " AND (name LIKE ? OR tag LIKE ?)"
        args += [f"%{q}%", f"%{q}%"]
    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))
    rows = db().execute(sql + " ORDER BY tag LIMIT ? OFFSET ?", args + [limit, offset]).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/assets/<tag>")
def get_asset(tag):
    row = db().execute("SELECT * FROM assets WHERE tag = ?", (tag,)).fetchone()
    if row is None:
        abort(404, description=f"no asset {tag}")
    return jsonify(dict(row))


@app.post("/api/assets")
def create_asset():
    data = validate(request.get_json(silent=True) or {})
    cols = ", ".join(data)
    try:
        with db():
            db().execute(f"INSERT INTO assets ({cols}) VALUES ({', '.join('?' * len(data))})",
                         list(data.values()))
    except sqlite3.IntegrityError:
        abort(409, description=f"tag {data['tag']} already exists")
    row = db().execute("SELECT * FROM assets WHERE tag = ?", (data["tag"],)).fetchone()
    return jsonify(dict(row)), 201


@app.patch("/api/assets/<tag>")
def update_asset(tag):
    data = validate(request.get_json(silent=True) or {}, partial=True)
    data.pop("tag", None)
    if not data:
        abort(400, description="nothing to update")
    sets = ", ".join(f"{k} = ?" for k in data)
    with db():
        n = db().execute(f"UPDATE assets SET {sets} WHERE tag = ?", [*data.values(), tag]).rowcount
    if n == 0:
        abort(404, description=f"no asset {tag}")
    return get_asset(tag)


@app.delete("/api/assets/<tag>")
def delete_asset(tag):
    with db():
        n = db().execute("DELETE FROM assets WHERE tag = ?", (tag,)).rowcount
    if n == 0:
        abort(404, description=f"no asset {tag}")
    return "", 204


@app.get("/api/stats")
def stats():
    rows = db().execute("SELECT category, COUNT(*) AS count, ROUND(SUM(cost), 2) AS total_cost "
                        "FROM assets GROUP BY category ORDER BY total_cost DESC").fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
