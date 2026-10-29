# sales_report.py
import numpy as np
import pandas as pd

def make_sample(path="orders.csv", n=1200, seed=7):
    rng = np.random.default_rng(seed)
    products = {"Laptop": 45000, "Phone": 18000, "Tablet": 22000, "Monitor": 9000, "Headset": 2500}
    df = pd.DataFrame({
        "order_date": pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 300, n), unit="D"),
        "region": rng.choice(["NCR", "Luzon", "Visayas", "Mindanao"], n, p=[.4, .25, .2, .15]),
        "product": rng.choice(list(products), n),
        "units": rng.integers(1, 15, n),
        "rep": rng.choice(["Ana", "Ben", "Cara", "Dan", "Eli"], n),
    })
    df["unit_price"] = df["product"].map(products)
    df.to_csv(path, index=False)

def build_report(src="orders.csv", out="sales_report.xlsx"):
    df = pd.read_csv(src, parse_dates=["order_date"])
    df = df.dropna().drop_duplicates()
    df["revenue"] = df["units"] * df["unit_price"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    monthly = df.groupby("month")["revenue"].sum().to_frame()
    monthly["growth"] = monthly["revenue"].pct_change()
    by_region = df.pivot_table(index="region", columns="product", values="revenue", aggfunc="sum", margins=True)
    reps = (df.groupby("rep").agg(orders=("revenue", "size"), revenue=("revenue", "sum"))
              .sort_values("revenue", ascending=False))
    reps["share"] = reps["revenue"] / reps["revenue"].sum()

    with pd.ExcelWriter(out) as xl:
        monthly.to_excel(xl, sheet_name="Monthly")
        by_region.to_excel(xl, sheet_name="Region x Product")
        reps.to_excel(xl, sheet_name="Sales reps")
        df.to_excel(xl, sheet_name="Raw data", index=False)

    best = monthly["revenue"].idxmax()
    print(f"Total revenue: {df['revenue'].sum():,.0f}")
    print(f"Best month: {best} ({monthly.loc[best, 'revenue']:,.0f})")
    print(f"Top rep: {reps.index[0]} ({reps['share'].iloc[0]:.0%} of revenue)")
    print(f"Report written to {out}")

if __name__ == "__main__":
    make_sample()
    build_report()
