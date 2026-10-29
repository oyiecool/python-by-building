with con:
    con.execute("UPDATE customers SET city = ? WHERE id = ?", ("Quezon City", 1))
    con.execute("DELETE FROM orders WHERE amount < ?", (100,))
