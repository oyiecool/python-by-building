def caesar(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

secret = caesar("Hello, World!", 3)     # 'Khoor, Zruog!'
print(caesar(secret, -3))               # decrypt with the negative shift
