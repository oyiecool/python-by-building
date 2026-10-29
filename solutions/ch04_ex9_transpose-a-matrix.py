m = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
t = [[row[c] for row in m] for c in range(len(m[0]))]
# [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]   (also: list(map(list, zip(*m))))
