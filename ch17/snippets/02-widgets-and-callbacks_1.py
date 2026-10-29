import tkinter as tk
from tkinter import ttk, messagebox

def greet():
    name = name_var.get().strip()
    if not name:
        messagebox.showwarning("Missing", "Please type your name.")
        return
    msg = f"Hello, {name}!" + (" Welcome back." if member_var.get() else "")
    result_var.set(msg)

root = tk.Tk()
root.title("Greeter")

name_var = tk.StringVar()
member_var = tk.BooleanVar()
result_var = tk.StringVar(value="...")

ttk.Label(root, text="Name:").grid(row=0, column=0, padx=8, pady=8, sticky="e")
entry = ttk.Entry(root, textvariable=name_var, width=25)
entry.grid(row=0, column=1, padx=8)
ttk.Checkbutton(root, text="Returning member", variable=member_var).grid(row=1, column=1, sticky="w")
ttk.Button(root, text="Greet", command=greet).grid(row=2, column=1, sticky="e", padx=8, pady=8)
ttk.Label(root, textvariable=result_var, font=("Segoe UI", 12)).grid(row=3, column=0, columnspan=2, pady=8)

entry.focus()
root.bind("<Return>", lambda event: greet())   # Enter key also greets
root.mainloop()
