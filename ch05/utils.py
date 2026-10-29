# utils.py
"""Small helpers used across the book."""

def format_bytes(n: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def is_valid_ip(text: str) -> bool:
    parts = text.split(".")
    return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

if __name__ == "__main__":
    # runs only when this file is executed directly, not when imported
    print(format_bytes(123456789))
    print(is_valid_ip("192.168.1.300"))
