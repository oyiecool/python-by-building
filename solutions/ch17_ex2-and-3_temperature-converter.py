import tkinter as tk
from tkinter import ttk

def convert(*_):
    try:
        value = float(entry_var.get())
    except ValueError:
        result.config(text="Enter a number")
        return
    if mode.get() == "C to F":
        result.config(text=f"{value:.1f} °C = {value * 9 / 5 + 32:.1f} °F")
    else:
        result.config(text=f"{value:.1f} °F = {(value - 32) * 5 / 9:.1f} °C")

root = tk.Tk()
root.title("Temperature converter")
entry_var, mode = tk.StringVar(), tk.StringVar(value="C to F")
ttk.Entry(root, textvariable=entry_var, width=12).grid(row=0, column=0, padx=8, pady=8)
ttk.Combobox(root, textvariable=mode, values=["C to F", "F to C"], state="readonly", width=8).grid(row=0, column=1)
ttk.Button(root, text="Convert", command=convert).grid(row=0, column=2, padx=8)
result = ttk.Label(root, text="", font=("Segoe UI", 14))
result.grid(row=1, column=0, columnspan=3, pady=8)
root.bind("<Return>", convert)
root.mainloop()
