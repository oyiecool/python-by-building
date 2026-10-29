sales["revenue"] = sales["qty"] * sales["price"]

by_region = sales.groupby("region")["revenue"].sum().sort_values(ascending=False)
print(by_region)

summary = sales.groupby("product").agg(
    orders=("qty", "count"),
    units=("qty", "sum"),
    revenue=("revenue", "sum"),
    avg_order=("revenue", "mean"),
)
print(summary.round(0))

print(sales["region"].value_counts())
