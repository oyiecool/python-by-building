from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = Figure(figsize=(5, 3))
ax = fig.add_subplot()
ax.bar(["Mon", "Tue", "Wed"], [12, 19, 7])
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill="both", expand=True)
canvas.draw()            # call again after changing the data
