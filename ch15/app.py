import json, os
from datetime import datetime
from pathlib import Path
from flask import Flask, request, redirect, url_for, flash, render_template, jsonify, abort

BASE = Path(__file__).resolve().parent
DATA = BASE / "tasks.json"
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
PRIORITIES = ["low", "normal", "high"]

def load_tasks() -> list[dict]:
    return json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else []

def save_tasks(tasks):
    DATA.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

def create_task(title: str, priority: str = "normal", owner: str = "") -> dict:
    tasks = load_tasks()
    task = {"id": max((t["id"] for t in tasks), default=0) + 1, "title": title,
            "priority": priority if priority in PRIORITIES else "normal",
            "owner": owner, "done": False,
            "created": datetime.now().isoformat(timespec="minutes")}
    tasks.append(task)
    save_tasks(tasks)
    return task

@app.route("/")
def index():
    show = request.args.get("show", "open")
    tasks = load_tasks()
    if show == "open":
        tasks = [t for t in tasks if not t["done"]]
    order = {p: i for i, p in enumerate(reversed(PRIORITIES))}
    tasks.sort(key=lambda t: (t["done"], order[t["priority"]], t["id"]))
    return render_template("tasks.html", tasks=tasks, show=show, priorities=PRIORITIES)

@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    if len(title) < 3:
        flash("Title must be at least 3 characters.")
    else:
        create_task(title, request.form.get("priority", "normal"), request.form.get("owner", "").strip())
        flash(f"Added: {title}")
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    else:
        abort(404)
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/stats")
def stats():
    tasks = load_tasks()
    done = sum(t["done"] for t in tasks)
    by_owner = {}
    for t in tasks:
        by_owner.setdefault(t["owner"] or "unassigned", [0, 0])[t["done"]] += 1
    return render_template("stats.html", total=len(tasks), done=done, by_owner=by_owner)

@app.get("/api/tasks")
def api_list():
    return jsonify(load_tasks())

@app.post("/api/tasks")
def api_create():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        abort(400, description="title is required")
    return jsonify(create_task(data["title"], data.get("priority", "normal"), data.get("owner", ""))), 201

if __name__ == "__main__":
    app.run(debug=True)
