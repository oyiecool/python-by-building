import time
import numpy as np

prices = np.random.default_rng(0).uniform(10, 500, 1_000_000)

t = time.perf_counter()
with_tax = [p * 1.12 for p in prices]          # Python loop
print(f"loop:  {time.perf_counter() - t:.3f} s")

t = time.perf_counter()
with_tax = prices * 1.12                        # one vectorized operation
print(f"numpy: {time.perf_counter() - t:.3f} s")
