def banner(word: str) -> str:
    line = "*" * (len(word) + 4)
    return f"{line}\n* {word} *\n{line}"

print(banner(input("Word: ")))
