import sqlite3
import pandas as pd

df = pd.read_csv("orders.csv")
con = sqlite3.connect("orders.db")
df.to_sql("orders", con, if_exists="replace", index=False)

sql = """SELECT region, SUM(units * unit_price) AS revenue
         FROM orders GROUP BY region ORDER BY revenue DESC"""
print(con.execute(sql).fetchall())
# [('NCR', 72552500), ('Luzon', 37735000), ('Visayas', 33625000), ('Mindanao', 24241500)]

df["revenue"] = df["units"] * df["unit_price"]
print(df.groupby("region")["revenue"].sum().sort_values(ascending=False))   # identical totals
