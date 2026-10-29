def collatz_length(n: int) -> int:
    steps = 1
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

best = max(range(1, 10_000), key=collatz_length)
print(best, collatz_length(best))       # 6171 262
