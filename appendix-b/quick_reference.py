# variables and types
n, x, s, ok, nothing = 42, 3.14, "text", True, None
# collections
lst, tup, dct, st = [1, 2], (1, 2), {"k": 1}, {1, 2}
# decisions
if x > 3 and ok:
    ...
elif not ok:
    ...
else:
    ...
label = "big" if x > 3 else "small"
# loops
for i, item in enumerate(lst, start=1): ...
for k, v in dct.items(): ...
while n > 0: n -= 1
# comprehensions
squares = [i * i for i in range(10) if i % 2]
# functions
def f(a, b=2, *args, key=None, **kwargs) -> int:
    """Docstring."""
    return a + b
# classes
from dataclasses import dataclass
@dataclass
class Point:
    x: float
    y: float = 0.0
# errors
try:
    risky()
except (ValueError, KeyError) as e:
    print(e)
else:
    print("no error")
finally:
    cleanup()
# files
with open("f.txt", encoding="utf-8") as fh:
    for line in fh: ...
# match
match command.split():
    case ["go", direction]: ...
    case _: ...
