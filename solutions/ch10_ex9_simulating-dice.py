import random
from collections import Counter

rolls = Counter(random.randint(1, 6) + random.randint(1, 6) for _ in range(100_000))
for total in range(2, 13):
    print(f"{total:>2} {rolls[total] / 1000:5.1f}% {'#' * (rolls[total] // 500)}")
