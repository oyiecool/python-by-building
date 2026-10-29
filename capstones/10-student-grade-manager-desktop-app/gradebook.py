# gradebook.py - Capstone 10
"""Student grade manager: SQLite storage, weighted grades, a Tkinter GUI and a live histogram."""
import csv
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "grades.db"
WEIGHTS = {"quiz": 0.30, "exam": 0.50, "project": 0.20}
LETTERS = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F")]


def letter(percent: float | None) -> str:
    if percent is None:
        return "-"
    return next(l for cutoff, l in LETTERS if percent >= cutoff)


class GradeBook:
    """All the logic, with no GUI code, so it can be tested on its own."""

    def __init__(self, path: Path | str = DB):
        self.con = sqlite3.connect(path)
        self.con.row_factory = sqlite3.Row
        self.con.executescript("""
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE,
                section TEXT NOT NULL DEFAULT '');
            CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                kind TEXT NOT NULL CHECK (kind IN ('quiz', 'exam', 'project')),
                title TEXT NOT NULL, score REAL NOT NULL, max_score REAL NOT NULL CHECK (max_score > 0));""")

    def add_student(self, name: str, section: str = "") -> int:
        with self.con:
            return self.con.execute("INSERT INTO students (name, section) VALUES (?, ?)",
                                    (name.strip().title(), section.strip())).lastrowid

    def remove_student(self, student_id: int) -> None:
        with self.con:
            self.con.execute("DELETE FROM students WHERE id = ?", (student_id,))

    def add_score(self, student_id: int, kind: str, title: str, score: float, max_score: float) -> None:
        if not 0 <= score <= max_score:
            raise ValueError("score must be between 0 and the maximum")
        with self.con:
            self.con.execute("INSERT INTO scores (student_id, kind, title, score, max_score) "
                             "VALUES (?, ?, ?, ?, ?)", (student_id, kind, title, score, max_score))

    def final_percent(self, student_id: int) -> float | None:
        """Weighted average of each category's percentage; missing categories are re-weighted."""
        rows = self.con.execute("SELECT kind, SUM(score) * 100.0 / SUM(max_score) AS pct FROM scores "
                                "WHERE student_id = ? GROUP BY kind", (student_id,)).fetchall()
        if not rows:
            return None
        weight = sum(WEIGHTS[r["kind"]] for r in rows)
        return round(sum(WEIGHTS[r["kind"]] * r["pct"] for r in rows) / weight, 1)

    def table(self) -> list[dict]:
        out = []
        for s in self.con.execute("SELECT * FROM students ORDER BY section, name"):
            pct = self.final_percent(s["id"])
            out.append({"id": s["id"], "name": s["name"], "section": s["section"],
                        "percent": pct, "letter": letter(pct)})
        return out

    def export_csv(self, path: Path | str) -> int:
        rows = self.table()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["name", "section", "percent", "letter"], extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        return len(rows)

    def seed_demo(self) -> None:
        import random
        random.seed(11)
        names = ["Ana Cruz", "Ben Santos", "Cara Reyes", "Dan Lim", "Eli Tan", "Fe Garcia",
                 "Gio Ramos", "Hana Uy", "Ivan Bautista", "Joy Mendoza", "Kiko Aquino", "Lea Villanueva"]
        for i, n in enumerate(names):
            sid = self.add_student(n, "BSIT-1A" if i % 2 == 0 else "BSIT-1B")
            skill = random.uniform(0.55, 0.98)
            for q in range(1, 5):
                self.add_score(sid, "quiz", f"Quiz {q}", round(min(20, random.gauss(skill * 20, 2))), 20)
            self.add_score(sid, "exam", "Midterm", round(min(100, max(0, random.gauss(skill * 100, 8)))), 100)
            self.add_score(sid, "exam", "Final", round(min(100, max(0, random.gauss(skill * 100, 8)))), 100)
            self.add_score(sid, "project", "Capstone", round(min(50, random.gauss(skill * 50 + 3, 4))), 50)


def run_gui(book: GradeBook) -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    root = tk.Tk()
    root.title("Grade Manager")
    root.geometry("1000x560")

    left = ttk.Frame(root, padding=10)
    left.pack(side="left", fill="y")
    name_var, section_var = tk.StringVar(), tk.StringVar(value="BSIT-1A")
    kind_var, title_var = tk.StringVar(value="quiz"), tk.StringVar()
    score_var, max_var = tk.StringVar(), tk.StringVar(value="20")

    box = ttk.LabelFrame(left, text="New student", padding=8)
    box.pack(fill="x")
    ttk.Label(box, text="Name").grid(row=0, column=0, sticky="w")
    ttk.Entry(box, textvariable=name_var, width=22).grid(row=0, column=1, pady=2)
    ttk.Label(box, text="Section").grid(row=1, column=0, sticky="w")
    ttk.Entry(box, textvariable=section_var, width=22).grid(row=1, column=1, pady=2)

    box2 = ttk.LabelFrame(left, text="Score for selected student", padding=8)
    box2.pack(fill="x", pady=10)
    ttk.Label(box2, text="Type").grid(row=0, column=0, sticky="w")
    ttk.Combobox(box2, textvariable=kind_var, values=list(WEIGHTS), state="readonly", width=19).grid(row=0, column=1, pady=2)
    for r, (label, var) in enumerate([("Title", title_var), ("Score", score_var), ("Out of", max_var)], start=1):
        ttk.Label(box2, text=label).grid(row=r, column=0, sticky="w")
        ttk.Entry(box2, textvariable=var, width=22).grid(row=r, column=1, pady=2)

    right = ttk.Frame(root, padding=10)
    right.pack(side="left", fill="both", expand=True)
    cols = ("name", "section", "percent", "letter")
    tree = ttk.Treeview(right, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (200, 90, 80, 60)):
        tree.heading(c, text=c.title())
        tree.column(c, width=w, anchor="w" if c in ("name", "section") else "center")
    tree.pack(fill="x")
    status = ttk.Label(right)
    status.pack(anchor="w", pady=4)

    fig = Figure(figsize=(6, 2.6), dpi=100)
    ax = fig.add_subplot()
    canvas = FigureCanvasTkAgg(fig, master=right)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh():
        tree.delete(*tree.get_children())
        rows = book.table()
        for r in rows:
            tree.insert("", "end", iid=r["id"],
                        values=(r["name"], r["section"], "" if r["percent"] is None else f"{r['percent']:.1f}", r["letter"]))
        grades = [r["percent"] for r in rows if r["percent"] is not None]
        ax.clear()
        ax.hist(grades, bins=range(40, 101, 5), color="#2b6cb0", edgecolor="white")
        for cutoff, l in LETTERS[:-1]:
            ax.axvline(cutoff, color="gray", linestyle=":", linewidth=1)
            ax.text(cutoff + 1, ax.get_ylim()[1] * 0.9, l, color="gray")
        avg = sum(grades) / len(grades) if grades else 0
        ax.set(title=f"Final grades: class average {avg:.1f}%", xlabel="%", ylabel="Students")
        fig.tight_layout()
        canvas.draw()
        failing = sum(g < 60 for g in grades)
        status.config(text=f"{len(rows)} students, {failing} below 60%")

    def selected_id() -> int | None:
        sel = tree.selection()
        return int(sel[0]) if sel else None

    def add_student():
        if not name_var.get().strip():
            messagebox.showwarning("Missing", "Type a name first.")
            return
        try:
            book.add_student(name_var.get(), section_var.get())
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate", "That student already exists.")
        name_var.set("")
        refresh()

    def add_score():
        sid = selected_id()
        if sid is None:
            messagebox.showinfo("Select", "Select a student in the table first.")
            return
        try:
            book.add_score(sid, kind_var.get(), title_var.get() or kind_var.get().title(),
                           float(score_var.get()), float(max_var.get()))
        except ValueError as e:
            messagebox.showerror("Invalid score", str(e))
            return
        score_var.set("")
        refresh()
        tree.selection_set(str(sid))

    def remove():
        sid = selected_id()
        if sid is not None and messagebox.askyesno("Remove", "Delete this student and all scores?"):
            book.remove_student(sid)
            refresh()

    def export():
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            messagebox.showinfo("Exported", f"{book.export_csv(path)} students written.")

    ttk.Button(box, text="Add student", command=add_student).grid(row=2, column=1, sticky="e", pady=4)
    ttk.Button(box2, text="Add score", command=add_score).grid(row=4, column=1, sticky="e", pady=4)
    ttk.Button(left, text="Remove selected student", command=remove).pack(fill="x")
    ttk.Button(left, text="Export report (CSV)...", command=export).pack(fill="x", pady=6)
    ttk.Label(left, text="Weights: " + ", ".join(f"{k} {v:.0%}" for k, v in WEIGHTS.items()),
              foreground="gray").pack(anchor="w", pady=10)
    refresh()
    root.mainloop()


if __name__ == "__main__":
    gb = GradeBook()
    if not gb.table():
        gb.seed_demo()
    run_gui(gb)
