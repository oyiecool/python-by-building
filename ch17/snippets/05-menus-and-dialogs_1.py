from tkinter import filedialog, messagebox, simpledialog

path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
save = filedialog.asksaveasfilename(defaultextension=".txt")
ok = messagebox.askyesno("Confirm", "Delete the selected item?")
age = simpledialog.askinteger("Age", "Your age?", minvalue=0, maxvalue=130)

menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=False)
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)
root.bind("<Control-o>", lambda e: open_file())
