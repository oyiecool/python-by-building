import tkinter as tk
from tkinter import ttk

WORK = 25 * 60

class Pomodoro:
    def __init__(self, root):
        self.root, self.left, self.running, self.job = root, WORK, False, None
        root.title("Pomodoro")
        self.label = ttk.Label(root, font=("Consolas", 48))
        self.label.pack(padx=30, pady=10)
        bar = ttk.Frame(root)
        bar.pack(pady=10)
        for text, cmd in (("Start", self.start), ("Pause", self.pause), ("Reset", self.reset)):
            ttk.Button(bar, text=text, command=cmd).pack(side="left", padx=4)
        self.show()

    def show(self):
        m, s = divmod(self.left, 60)
        self.label.config(text=f"{m:02d}:{s:02d}")

    def tick(self):
        if not self.running:
            return
        self.left -= 1
        self.show()
        if self.left == 0:
            self.running = False
            self.root.bell()
            self.label.config(text="Break!")
        else:
            self.job = self.root.after(1000, self.tick)

    def start(self):
        if not self.running and self.left > 0:
            self.running = True
            self.job = self.root.after(1000, self.tick)

    def pause(self):
        self.running = False
        if self.job:
            self.root.after_cancel(self.job)

    def reset(self):
        self.pause()
        self.left = WORK
        self.show()

root = tk.Tk()
Pomodoro(root)
root.mainloop()
