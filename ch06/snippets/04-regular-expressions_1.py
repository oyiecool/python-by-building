import re

text = "Contact ana@example.com or ben.cruz@company.ph by 2026-11-15."

emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print(emails)          # ['ana@example.com', 'ben.cruz@company.ph']

m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
if m:
    year, month, day = m.groups()
    print(year, month, day)

clean = re.sub(r"\s+", " ", "too    many     spaces")
print(clean)

print(re.fullmatch(r"09\d{9}", "09171234567") is not None)  # PH mobile format
