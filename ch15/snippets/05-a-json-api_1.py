from flask import jsonify, abort

@app.get("/api/tasks")
def api_list():
    return jsonify(load_tasks())

@app.post("/api/tasks")
def api_create():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        abort(400, description="title is required")
    task = create_task(data["title"], data.get("priority", "normal"))
    return jsonify(task), 201
