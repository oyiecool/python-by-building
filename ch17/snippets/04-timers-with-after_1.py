import tkinter as tk
from datetime import datetime

root = tk.Tk()
root.title("Clock")
clock = tk.Label(root, font=("Consolas", 40), padx=20, pady=10)
clock.pack()

def tick():
    clock.config(text=datetime.now().strftime("%H:%M:%S"))
    root.after(1000, tick)        # call tick again in 1000 ms

tick()
root.mainloop()
