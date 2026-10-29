def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32

def top_n(scores: dict[str, int], n: int = 3) -> list[str]:
    return sorted(scores, key=scores.get, reverse=True)[:n]
