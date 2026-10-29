import numpy as np

a = np.array([3, 1, 4, 1, 5, 9])
print(a.shape, a.dtype, a.ndim)      # (6,) int64 1

grid = np.array([[1, 2, 3], [4, 5, 6]])
print(grid.shape)                    # (2, 3): 2 rows, 3 columns

np.zeros((3, 4))                     # 3x4 of 0.0
np.ones(5, dtype=int)                # [1 1 1 1 1]
np.arange(0, 1, 0.25)                # [0.   0.25 0.5  0.75]
np.linspace(0, 1, 5)                 # 5 evenly spaced points, ends included
np.arange(12).reshape(3, 4)          # 0..11 as 3 rows x 4 columns
