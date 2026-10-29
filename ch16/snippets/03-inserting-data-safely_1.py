with con:                                        # a transaction: commits, or rolls back on error
    con.execute("INSERT INTO customers (name, city) VALUES (?, ?)", ("Ana Cruz", "Manila"))
    con.executemany("INSERT INTO customers (name, city) VALUES (?, ?)",
                    [("Ben Santos", "Cebu"), ("Cara Reyes", "Davao")])
    cur = con.execute("INSERT INTO orders (customer_id, item, amount) VALUES (?, ?, ?)", (1, "Laptop", 45000))
    print("new order id:", cur.lastrowid)
