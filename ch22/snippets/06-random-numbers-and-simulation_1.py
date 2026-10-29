rng = np.random.default_rng(seed=42)
rng.integers(1, 7, size=10)            # ten dice rolls
rng.normal(loc=170, scale=8, size=5)   # heights, mean 170 cm
rng.uniform(0, 1, size=(2, 3))
rng.choice(["heads", "tails"], size=4)
rng.triangular(2, 4, 9, size=3)        # min, most likely, max
