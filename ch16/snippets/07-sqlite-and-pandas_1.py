import pandas as pd
df = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["ordered_at"])
print(df.groupby("item")["amount"].sum())

# load a CSV into a new table
pd.read_csv("orders.csv").to_sql("big_orders", con, if_exists="replace", index=False)
