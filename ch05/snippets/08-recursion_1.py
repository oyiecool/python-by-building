def factorial(n: int) -> int:
    if n <= 1:                 # base case
        return 1
    return n * factorial(n - 1)

def folder_size(path):
    """Total bytes in a folder and all sub-folders."""
    import os
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)   # recursion
    return total

print(factorial(10))
print(f"{folder_size('.') / 1024:.1f} KB")
