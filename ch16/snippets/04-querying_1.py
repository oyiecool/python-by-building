con.row_factory = sqlite3.Row                    # rows behave like dicts
for row in con.execute("SELECT id, name, city FROM customers ORDER BY name"):
    print(row["id"], row["name"], row["city"])

one = con.execute("SELECT * FROM customers WHERE id = ?", (2,)).fetchone()
count = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
