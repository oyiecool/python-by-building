import pandas as pd

sales = pd.DataFrame({
    "date": pd.to_datetime(["2026-01-05", "2026-01-12", "2026-02-03", "2026-02-17", "2026-03-09", "2026-03-21"]),
    "region": ["North", "South", "North", "East", "South", "East"],
    "product": ["Laptop", "Phone", "Phone", "Laptop", "Tablet", "Phone"],
    "units": [3, 10, 7, 2, 5, 12],
    "price": [45000, 18000, 18000, 45000, 22000, 18000],
})

print(sales.head())        # first 5 rows
print(sales.shape)         # (6, 5)
print(sales.dtypes)
sales.info()
print(sales.describe())    # count, mean, std, min, quartiles, max
