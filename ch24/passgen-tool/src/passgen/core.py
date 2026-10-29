import math
import secrets
import string

SYMBOLS = "!@#$%^&*-_=+?"
WORDS = ("anchor bamboo canyon dragon ember falcon garnet harbor island jungle kettle lantern meadow "
         "nectar orbit pebble quartz river saddle timber umbrella velvet walnut yonder zephyr basil "
         "cobalt dune fennel glacier hazel ivory juniper koala lagoon mango nimbus olive prism quill "
         "raven sierra tundra violet willow").split()


def password(length: int = 16, symbols: bool = True) -> str:
    if length < 8:
        raise ValueError("length must be at least 8")
    pool = string.ascii_letters + string.digits + (SYMBOLS if symbols else "")
    while True:
        pw = "".join(secrets.choice(pool) for _ in range(length))
        if (any(c.islower() for c in pw) and any(c.isupper() for c in pw)
                and any(c.isdigit() for c in pw) and (not symbols or any(c in SYMBOLS for c in pw))):
            return pw


def passphrase(words: int = 5, sep: str = "-") -> str:
    if words < 3:
        raise ValueError("use at least 3 words")
    return sep.join(secrets.choice(WORDS) for _ in range(words))


def entropy_bits(choices: int, length: int) -> float:
    return length * math.log2(choices)
