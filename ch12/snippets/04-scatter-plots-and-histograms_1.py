import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
ad_spend = rng.uniform(5, 50, 60)                    # thousands
sales = 3.2 * ad_spend + rng.normal(0, 12, 60)

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))
left.scatter(ad_spend, sales, alpha=0.7)
m, b = np.polyfit(ad_spend, sales, 1)               # best-fit line
xs = np.linspace(5, 50, 100)
left.plot(xs, m * xs + b, color="crimson", label=f"y = {m:.1f}x + {b:.0f}")
left.set(title="Sales rise with ad spend", xlabel="Ad spend (k)", ylabel="Sales (k)")
left.legend()

right.hist(sales, bins=12, edgecolor="white")
right.axvline(sales.mean(), color="black", linestyle="--", label=f"mean {sales.mean():.0f}")
right.set(title="Distribution of weekly sales", xlabel="Sales (k)", ylabel="Weeks")
right.legend()
fig.tight_layout()
plt.show()
