from flask import request, redirect, url_for, flash, render_template

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Title is required.")
    else:
        ...  # save it
        flash(f"Added: {title}")
    return redirect(url_for("index"))
