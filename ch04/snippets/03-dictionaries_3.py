words = "the cat and the hat and the bat".split()
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)   # {'the': 3, 'cat': 1, 'and': 2, 'hat': 1, 'bat': 1}
