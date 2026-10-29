import matplotlib.pyplot as plt

products = ["Laptop", "Tablet", "Phone", "Monitor", "Headset"]
revenue_m = [76.5, 36.0, 33.5, 17.8, 4.3]
colors = ["#2b6cb0" if p == "Laptop" else "#b0b7c3" for p in products]

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(products[::-1], revenue_m[::-1], color=colors[::-1])
ax.bar_label(bars, fmt="%.1fM", padding=4)
ax.set_title("Laptops bring in 45% of revenue", loc="left", fontweight="bold")
ax.set_xlabel("Revenue (millions)")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("revenue_by_product.png", dpi=150)
plt.show()
