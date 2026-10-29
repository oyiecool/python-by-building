pivot = sales.pivot_table(index="month", columns="region", values="revenue",
                          aggfunc="sum", fill_value=0, margins=True)
print(pivot)
print(pd.crosstab(sales["region"], sales["product"]))
