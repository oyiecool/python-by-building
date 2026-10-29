sales["units"]                         # one column (Series)
sales[["region", "units"]]             # several columns (DataFrame)
sales.loc[0]                           # row by label
sales.iloc[-1]                         # row by position
sales.loc[sales["units"] > 5, ["product", "units"]]

big_north = sales[(sales["region"] == "North") & (sales["units"] >= 5)]
phones_or_tablets = sales[sales["product"].isin(["Phone", "Tablet"])]
q = sales.query("units > 4 and price < 30000")
