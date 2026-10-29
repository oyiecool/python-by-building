# contacts.py
import sqlite3, csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

DB = Path(__file__).resolve().parent / "contacts.db"
FIELDS = ("name", "phone", "email", "company")

class ContactBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Book")
        self.geometry("760x460")
        self.con = sqlite3.connect(DB)
        self.con.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, "
                         "name TEXT NOT NULL, phone TEXT, email TEXT, company TEXT)")
        self.vars = {f: tk.StringVar() for f in FIELDS}
        self.search_var = tk.StringVar()
        self.selected_id = None
        self._build()
        self.refresh()

    def _build(self):
        form = ttk.LabelFrame(self, text="Details", padding=10)
        form.pack(side="left", fill="y", padx=10, pady=10)
        for i, f in enumerate(FIELDS):
            ttk.Label(form, text=f.title() + ":").grid(row=i, column=0, sticky="e", pady=4)
            ttk.Entry(form, textvariable=self.vars[f], width=26).grid(row=i, column=1, pady=4)
        buttons = ttk.Frame(form)
        buttons.grid(row=len(FIELDS), column=0, columnspan=2, pady=10)
        for text, cmd in [("Add", self.add), ("Update", self.update_contact),
                          ("Delete", self.delete), ("Clear", self.clear)]:
            ttk.Button(buttons, text=text, command=cmd, width=8).pack(side="left", padx=2)
        ttk.Button(form, text="Export CSV...", command=self.export).grid(
            row=len(FIELDS) + 1, column=0, columnspan=2, sticky="ew")

        right = ttk.Frame(self)
        right.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        top = ttk.Frame(right)
        top.pack(fill="x")
        ttk.Label(top, text="Search:").pack(side="left")
        ttk.Entry(top, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=5)
        self.search_var.trace_add("write", lambda *a: self.refresh())   # live search

        self.tree = ttk.Treeview(right, columns=FIELDS, show="headings")
        for f in FIELDS:
            self.tree.heading(f, text=f.title(), command=lambda c=f: self.refresh(order=c))
            self.tree.column(f, width=110)
        self.tree.pack(fill="both", expand=True, pady=(8, 0))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.status = ttk.Label(right, text="")
        self.status.pack(anchor="w")

    def values(self):
        return [self.vars[f].get().strip() for f in FIELDS]

    def refresh(self, order="name"):
        self.tree.delete(*self.tree.get_children())
        q = f"%{self.search_var.get().strip()}%"
        rows = self.con.execute(
            f"SELECT id, {', '.join(FIELDS)} FROM contacts "
            "WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR company LIKE ? "
            f"ORDER BY {order if order in FIELDS else 'name'} COLLATE NOCASE", (q, q, q, q)).fetchall()
        for row in rows:
            self.tree.insert("", "end", iid=row[0], values=row[1:])
        self.status.config(text=f"{len(rows)} contact(s)")

    def on_select(self, _event):
        sel = self.tree.selection()
        if sel:
            self.selected_id = int(sel[0])
            for f, v in zip(FIELDS, self.tree.item(sel[0], "values")):
                self.vars[f].set(v)

    def add(self):
        vals = self.values()
        if not vals[0]:
            messagebox.showwarning("Missing", "Name is required.")
            return
        with self.con:
            self.con.execute("INSERT INTO contacts (name, phone, email, company) VALUES (?, ?, ?, ?)", vals)
        self.clear()
        self.refresh()

    def update_contact(self):
        if self.selected_id is None:
            return
        with self.con:
            self.con.execute("UPDATE contacts SET name=?, phone=?, email=?, company=? WHERE id=?",
                             (*self.values(), self.selected_id))
        self.refresh()

    def delete(self):
        if self.selected_id is None or not messagebox.askyesno("Delete", "Delete this contact?"):
            return
        with self.con:
            self.con.execute("DELETE FROM contacts WHERE id=?", (self.selected_id,))
        self.clear()
        self.refresh()

    def clear(self):
        self.selected_id = None
        for v in self.vars.values():
            v.set("")

    def export(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            rows = self.con.execute(f"SELECT {', '.join(FIELDS)} FROM contacts ORDER BY name").fetchall()
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(FIELDS)
                w.writerows(rows)
            messagebox.showinfo("Exported", f"{len(rows)} contacts saved.")

if __name__ == "__main__":
    ContactBook().mainloop()
