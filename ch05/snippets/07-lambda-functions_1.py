people = [("Ana", 31), ("Ben", 25), ("Cara", 40)]
by_age = sorted(people, key=lambda p: p[1])
oldest = max(people, key=lambda p: p[1])
adults = list(filter(lambda p: p[1] >= 30, people))
doubled = list(map(lambda x: x * 2, [1, 2, 3]))
