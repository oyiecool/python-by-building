import string

def password_strength(pw: str) -> tuple[int, list[str]]:
    checks = {
        "at least 8 characters": len(pw) >= 8,
        "an uppercase letter": any(c.isupper() for c in pw),
        "a lowercase letter": any(c.islower() for c in pw),
        "a digit": any(c.isdigit() for c in pw),
        "a symbol": any(c in string.punctuation for c in pw),
    }
    return sum(checks.values()), [f"Add {k}" for k, ok in checks.items() if not ok]

if __name__ == "__main__":
    print(password_strength("hello"))        # (1, ['Add at least 8 characters', ...])
    print(password_strength("Tr0ub4dor&3"))  # (5, [])
