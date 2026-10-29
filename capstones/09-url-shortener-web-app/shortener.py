# shortener.py - Capstone 9
"""A small URL shortener: short codes, click counting, per-link stats, and a JSON API."""
import os
import secrets
import sqlite3
import string
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, abort, flash, g, jsonify, redirect, render_template_string, request, url_for

DB = Path(os.environ.get("SHORTENER_DB", Path(__file__).resolve().parent / "links.db"))
ALPHABET = string.ascii_letters + string.digits          # 62 symbols; 6 chars = 56.8 billion codes
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Shorty</title>
<style>body{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem}
input[type=url]{width:60%}table{width:100%;border-collapse:collapse}td,th{padding:.35rem;border-bottom:1px solid #ddd;text-align:left}
.flash{background:#eef6ff;padding:.5rem;border-radius:6px}</style></head><body>
<h1>Shorty</h1>
{% for m in get_flashed_messages() %}<p class="flash">{{ m }}</p>{% endfor %}
<form method="post" action="{{ url_for('shorten') }}">
  <input type="url" name="url" placeholder="https://example.com/a/very/long/link" required>
  <input name="code" placeholder="custom code (optional)" pattern="[A-Za-z0-9_-]{3,20}">
  <button>Shorten</button></form>
<h2>Recent links</h2>
<table><tr><th>Short</th><th>Target</th><th>Clicks</th><th>Created</th></tr>
{% for l in links %}<tr><td><a href="{{ url_for('follow', code=l.code) }}">{{ request.host }}/{{ l.code }}</a>
 (<a href="{{ url_for('stats', code=l.code) }}">stats</a>)</td>
 <td>{{ l.url[:50] }}</td><td>{{ l.clicks }}</td><td>{{ l.created_at[:16] }}</td></tr>{% endfor %}
</table></body></html>"""


def db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.executescript("""
            CREATE TABLE IF NOT EXISTS links (code TEXT PRIMARY KEY, url TEXT NOT NULL,
                created_at TEXT NOT NULL, clicks INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS clicks (code TEXT NOT NULL REFERENCES links(code),
                at TEXT NOT NULL, referrer TEXT, agent TEXT);""")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    if (con := g.pop("db", None)) is not None:
        con.close()


def valid_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in ("http", "https") and bool(p.netloc)


def new_code(length: int = 6) -> str:
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if not db().execute("SELECT 1 FROM links WHERE code = ?", (code,)).fetchone():
            return code


def create(url: str, code: str | None = None) -> str:
    if not valid_url(url):
        raise ValueError("Only http:// and https:// URLs can be shortened.")
    if code:
        if not (3 <= len(code) <= 20 and all(c in ALPHABET + "_-" for c in code)):
            raise ValueError("Custom codes use 3-20 letters, digits, _ or -.")
        if db().execute("SELECT 1 FROM links WHERE code = ?", (code,)).fetchone():
            raise ValueError(f"The code '{code}' is taken.")
    code = code or new_code()
    with db():
        db().execute("INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
                     (code, url, datetime.now().isoformat(timespec="seconds")))
    return code


@app.get("/")
def index():
    links = db().execute("SELECT * FROM links ORDER BY created_at DESC LIMIT 20").fetchall()
    return render_template_string(PAGE, links=links)


@app.post("/shorten")
def shorten():
    try:
        code = create(request.form["url"].strip(), request.form.get("code", "").strip() or None)
        flash(f"Created {request.host_url}{code}")
    except ValueError as e:
        flash(str(e))
    return redirect(url_for("index"))


@app.get("/<code>")
def follow(code):
    row = db().execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
    if row is None:
        abort(404)
    with db():
        db().execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))
        db().execute("INSERT INTO clicks VALUES (?, ?, ?, ?)",
                     (code, datetime.now().isoformat(timespec="seconds"),
                      request.referrer or "", request.user_agent.string[:200]))
    return redirect(row["url"], code=302)


@app.get("/<code>/stats")
def stats(code):
    link = db().execute("SELECT * FROM links WHERE code = ?", (code,)).fetchone()
    if link is None:
        abort(404)
    per_day = db().execute("SELECT substr(at, 1, 10) AS day, COUNT(*) AS n FROM clicks "
                           "WHERE code = ? GROUP BY day ORDER BY day", (code,)).fetchall()
    return jsonify(code=code, url=link["url"], clicks=link["clicks"],
                   created_at=link["created_at"], per_day={r["day"]: r["n"] for r in per_day})


@app.post("/api/links")
def api_create():
    data = request.get_json(silent=True) or {}
    try:
        code = create(str(data.get("url", "")), data.get("code"))
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(code=code, short_url=f"{request.host_url}{code}"), 201


if __name__ == "__main__":
    app.run(debug=True)
