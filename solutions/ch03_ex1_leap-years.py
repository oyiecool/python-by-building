def is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

print([y for y in (1900, 2000, 2024, 2026) if is_leap(y)])   # [2000, 2024]
