# write
with open("todo.txt", "w", encoding="utf-8") as f:
    f.write("Buy milk\n")
    f.write("Patch servers\n")

# append
with open("todo.txt", "a", encoding="utf-8") as f:
    f.write("Call Ana\n")

# read everything
with open("todo.txt", encoding="utf-8") as f:
    content = f.read()

# read line by line (memory-friendly for huge files)
with open("todo.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.rstrip("\n"))
