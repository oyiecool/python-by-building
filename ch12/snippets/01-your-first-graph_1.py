import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
visitors = [1200, 1350, 1800, 1650, 2100, 2400]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, visitors, marker="o", linewidth=2)
ax.set_title("Website visitors doubled in six months")
ax.set_xlabel("Month")
ax.set_ylabel("Visitors")
ax.grid(alpha=0.3)
fig.tight_layout()
plt.show()
