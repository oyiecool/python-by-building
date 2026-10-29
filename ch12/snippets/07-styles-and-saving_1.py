print(plt.style.available)
plt.style.use("seaborn-v0_8-whitegrid")   # or "ggplot", "fivethirtyeight"
fig.savefig("chart.png", dpi=200, bbox_inches="tight")   # for documents
fig.savefig("chart.svg")                                 # scalable, for the web
fig.savefig("chart.pdf")                                 # for print
