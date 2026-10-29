# passgen.py
import argparse
import secrets
import string
import math

def generate(length: int, symbols: bool, avoid_ambiguous: bool) -> str:
    pool = string.ascii_letters + string.digits + ("!@#$%^&*-_=+?" if symbols else "")
    if avoid_ambiguous:
        pool = "".join(c for c in pool if c not in "Il1O0o")
    while True:
        pw = "".join(secrets.choice(pool) for _ in range(length))
        if (any(c.islower() for c in pw) and any(c.isupper() for c in pw)
                and any(c.isdigit() for c in pw)):
            return pw

def entropy_bits(length: int, pool_size: int) -> float:
    return length * math.log2(pool_size)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate strong passwords")
    p.add_argument("-l", "--length", type=int, default=16)
    p.add_argument("-c", "--count", type=int, default=5)
    p.add_argument("--no-symbols", action="store_true")
    p.add_argument("--no-ambiguous", action="store_true")
    a = p.parse_args()
    pool = 62 + (0 if a.no_symbols else 13) - (6 if a.no_ambiguous else 0)
    print(f"Entropy per password: {entropy_bits(a.length, pool):.0f} bits")
    for _ in range(a.count):
        print(generate(a.length, not a.no_symbols, a.no_ambiguous))
