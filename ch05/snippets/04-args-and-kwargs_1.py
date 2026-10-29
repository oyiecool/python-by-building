def average(*numbers):               # any number of positional args -> tuple
    return sum(numbers) / len(numbers) if numbers else 0

def build_tag(tag, text, **attrs):   # any keyword args -> dict
    attr_text = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<{tag} {attr_text}>{text}</{tag}>"

print(average(3, 4, 5, 6))
print(build_tag("a", "Docs", href="https://python.org", target="_blank"))

values = [10, 20, 30]
print(average(*values))              # unpack a list into arguments
