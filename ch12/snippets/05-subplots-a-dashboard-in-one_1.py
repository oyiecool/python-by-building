fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].plot(...)     # top-left
axes[0, 1].bar(...)      # top-right
axes[1, 0].scatter(...)  # bottom-left
axes[1, 1].pie(...)      # bottom-right
fig.suptitle("Monthly operations dashboard", fontsize=16)
fig.tight_layout()
