import pandas as pd
df = pd.read_csv("orders.csv", parse_dates=["order_date"])
df["revenue"] = df["units"] * df["unit_price"]

monthly = df.set_index("order_date").resample("ME")["revenue"].sum() / 1e6
ax = monthly.plot(kind="line", marker="o", figsize=(9, 4), title="Monthly revenue (millions)")
ax.set_ylim(0)

by_region = df.pivot_table(index=df["order_date"].dt.month, columns="region",
                           values="revenue", aggfunc="sum") / 1e6
by_region.plot(kind="bar", stacked=True, figsize=(10, 4), title="Revenue by region and month")
