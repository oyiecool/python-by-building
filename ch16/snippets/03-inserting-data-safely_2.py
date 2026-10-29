# WRONG - injectable
con.execute(f"SELECT * FROM customers WHERE name = '{user_input}'")
# RIGHT
con.execute("SELECT * FROM customers WHERE name = ?", (user_input,))
