# typing_trainer.py - Capstone 11
"""Typing speed trainer: live words-per-minute, accuracy, error highlighting and saved history."""
import json
import random
import time
from datetime import datetime
from pathlib import Path

HISTORY = Path(__file__).resolve().parent / "typing_history.json"
TEXTS = [
    "Python is a programming language that lets you work quickly and integrate systems more effectively.",
    "Simple is better than complex, and complex is better than complicated.",
    "A backup that has never been restored is only a hope, not a backup.",
    "Readability counts, so write code for the person who will maintain it next year.",
    "The quick brown fox jumps over the lazy dog while the server reboots at midnight.",
    "Errors should never pass silently unless they are explicitly silenced.",
    "Automate the boring parts of your job and spend the saved time learning something new.",
]


# ---------- logic (no GUI, easy to test) ----------
def wpm(chars_typed: int, seconds: float) -> float:
    """Standard definition: one 'word' = 5 characters, including spaces."""
    return 0.0 if seconds <= 0 else (chars_typed / 5) / (seconds / 60)


def accuracy(target: str, typed: str) -> float:
    if not typed:
        return 100.0
    correct = sum(a == b for a, b in zip(target, typed))
    return 100 * correct / len(typed)


def mistakes(target: str, typed: str) -> list[int]:
    """Positions of wrong characters, used to colour them red."""
    return [i for i, (a, b) in enumerate(zip(target, typed)) if a != b]


def load_history() -> list[dict]:
    try:
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return []


def save_result(speed: float, acc: float) -> list[dict]:
    hist = load_history()
    hist.append({"when": datetime.now().isoformat(timespec="seconds"), "wpm": round(speed, 1), "accuracy": round(acc, 1)})
    HISTORY.write_text(json.dumps(hist, indent=1), encoding="utf-8")
    return hist


# ---------- GUI ----------
class Trainer:
    def __init__(self):
        import tkinter as tk
        from tkinter import ttk
        self.tk = tk
        self.root = tk.Tk()
        self.root.title("Typing Trainer")
        self.root.geometry("820x420")
        self.target = ""
        self.start = None
        self.done = False

        self.text = tk.Text(self.root, height=4, wrap="word", font=("Consolas", 16), padx=10, pady=10,
                            relief="flat", background="#f4f6f8")
        self.text.pack(fill="x", padx=16, pady=(16, 8))
        self.text.tag_configure("ok", foreground="#2e7d32")
        self.text.tag_configure("bad", foreground="white", background="#c62828")
        self.text.tag_configure("cursor", underline=True)

        self.entry = tk.Text(self.root, height=3, wrap="word", font=("Consolas", 16), padx=10, pady=10)
        self.entry.pack(fill="x", padx=16)
        self.entry.bind("<KeyRelease>", self.on_key)

        self.stats = ttk.Label(self.root, font=("Segoe UI", 14))
        self.stats.pack(pady=10)
        self.best = ttk.Label(self.root, foreground="gray")
        self.best.pack()
        bar = ttk.Frame(self.root)
        bar.pack(pady=10)
        ttk.Button(bar, text="New text (Ctrl+N)", command=self.new_text).pack(side="left", padx=5)
        ttk.Button(bar, text="Show progress chart", command=self.chart).pack(side="left", padx=5)
        self.root.bind("<Control-n>", lambda e: self.new_text())
        self.new_text()
        self.tick()

    def new_text(self):
        self.target = random.choice([t for t in TEXTS if t != self.target])
        self.start, self.done = None, False
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", self.target)
        self.text.config(state="disabled")
        self.entry.config(state="normal")
        self.entry.delete("1.0", "end")
        self.entry.focus()
        hist = load_history()
        if hist:
            best = max(h["wpm"] for h in hist)
            avg = sum(h["wpm"] for h in hist[-10:]) / len(hist[-10:])
            self.best.config(text=f"Best {best:.0f} WPM   Last-10 average {avg:.0f} WPM   ({len(hist)} tests)")
        self.stats.config(text="Start typing: the timer starts with your first key.")

    def typed(self) -> str:
        return self.entry.get("1.0", "end-1c")

    def on_key(self, _event):
        if self.done:
            return
        typed = self.typed()
        if typed and self.start is None:
            self.start = time.perf_counter()
        self.text.tag_remove("ok", "1.0", "end")
        self.text.tag_remove("bad", "1.0", "end")
        self.text.tag_remove("cursor", "1.0", "end")
        bad = set(mistakes(self.target, typed))
        for i in range(min(len(typed), len(self.target))):
            self.text.tag_add("bad" if i in bad else "ok", f"1.0+{i}c")
        self.text.tag_add("cursor", f"1.0+{len(typed)}c")
        if len(typed) >= len(self.target):
            self.finish()

    def tick(self):
        if self.start and not self.done:
            secs = time.perf_counter() - self.start
            typed = self.typed()
            self.stats.config(text=f"{wpm(len(typed), secs):5.0f} WPM   {accuracy(self.target, typed):5.1f}% accurate   {secs:4.0f} s")
        self.root.after(200, self.tick)

    def finish(self):
        self.done = True
        secs = time.perf_counter() - self.start
        typed = self.typed()[:len(self.target)]
        speed, acc = wpm(len(typed), secs), accuracy(self.target, typed)
        net = speed * acc / 100
        save_result(net, acc)
        self.entry.config(state="disabled")
        self.stats.config(text=f"Done: {speed:.0f} WPM, {acc:.1f}% accuracy, net {net:.0f} WPM. Ctrl+N for another.")

    def chart(self):
        import matplotlib.pyplot as plt
        hist = load_history()
        if len(hist) < 2:
            self.stats.config(text="Do at least two tests to see a chart.")
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(range(1, len(hist) + 1), [h["wpm"] for h in hist], marker="o", label="Net WPM")
        ax.set(title="Your typing speed over time", xlabel="Test number", ylabel="Net words per minute")
        ax.set_ylim(0)
        ax.legend()
        plt.show()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Trainer().run()
