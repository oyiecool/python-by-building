import tkinter as tk

root = tk.Tk()
root.title("Hello Tkinter")
root.geometry("320x120")

label = tk.Label(root, text="Hello, desktop!", font=("Segoe UI", 16))
label.pack(pady=20)

root.mainloop()        # hands control to Tkinter until the window closes
