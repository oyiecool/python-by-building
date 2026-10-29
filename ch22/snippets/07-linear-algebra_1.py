# 2 coffees + 1 cake = 290;  1 coffee + 3 cakes = 420
A = np.array([[2, 1], [1, 3]])
b = np.array([290, 420])
coffee, cake = np.linalg.solve(A, b)
print(coffee, cake)                     # 90.0 110.0
