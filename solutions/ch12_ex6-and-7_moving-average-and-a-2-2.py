import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("orders.csv", parse_dates=["order_date"])
df["revenue"] = df["units"] * df["unit_price"]
monthly = df.set_index("order_date").resample("ME")["revenue"].sum() / 1e6

fig, axes = plt.subplots(2, 2, figsize=(13, 8))
ax = axes[0, 0]
ax.plot(monthly.index, monthly, marker="o", label="Monthly")
ax.plot(monthly.index, monthly.rolling(3).mean(), linestyle="--", label="3-month average")
ax.set(title="Revenue by month (millions)", ylim=(0, None))
ax.legend()
df.groupby("region")["revenue"].sum().sort_values().div(1e6).plot.barh(ax=axes[0, 1], title="By region (millions)")
df.groupby("product")["revenue"].sum().sort_values().div(1e6).plot.barh(ax=axes[1, 0], title="By product (millions)")
axes[1, 1].hist(df["units"], bins=range(1, 16), edgecolor="white")
axes[1, 1].set(title="Order size distribution", xlabel="Units per order", ylabel="Orders")
fig.tight_layout()
fig.savefig("dashboard.png", dpi=120)
plt.show()
