import re
PH_MOBILE = re.compile(r"(?:09|\+639)\d{9}")
for n in ("09171234567", "+639171234567", "0917123456"):
    print(n, bool(PH_MOBILE.fullmatch(n)))   # True, True, False
