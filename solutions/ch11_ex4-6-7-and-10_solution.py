import pandas as pd
df = pd.read_csv("orders.csv", parse_dates=["order_date"])
df["revenue"] = df["units"] * df["unit_price"]

# 4: busiest weekday
print(df["order_date"].dt.day_name().value_counts().head(1))

# 6: average units per order by product
print(df.groupby("product")["units"].mean().sort_values(ascending=False).round(2))

# 7: reps by month
print(df.pivot_table(index="rep", columns=df["order_date"].dt.month,
                     values="revenue", aggfunc="sum", fill_value=0))

# 10: growth per region and each region's best month
df["month"] = df["order_date"].dt.to_period("M")
monthly = df.groupby(["region", "month"])["revenue"].sum().unstack("region")
growth = monthly.pct_change().round(3)
best = monthly.idxmax().astype(str)
with pd.ExcelWriter("region_analysis.xlsx") as xl:
    growth.to_excel(xl, sheet_name="MoM growth")
    best.to_frame("best month").to_excel(xl, sheet_name="Best month")
