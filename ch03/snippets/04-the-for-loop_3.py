tasks = ["backup", "update", "reboot"]
for number, task in enumerate(tasks, start=1):
    print(f"{number}. {task}")

names = ["Ana", "Ben", "Cara"]
scores = [88, 92, 79]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
