sales["revenue"] = sales["units"] * sales["price"]
sales["month"] = sales["date"].dt.to_period("M").astype(str)
sales["size"] = sales["units"].apply(lambda u: "bulk" if u >= 10 else "normal")
sales = sales.sort_values(["revenue"], ascending=False)
sales = sales.rename(columns={"units": "qty"})
