import argparse

from . import __version__
from .core import SYMBOLS, WORDS, entropy_bits, passphrase, password


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="passgen", description="Generate strong passwords")
    ap.add_argument("-l", "--length", type=int, default=16)
    ap.add_argument("-c", "--count", type=int, default=1)
    ap.add_argument("--no-symbols", action="store_true")
    ap.add_argument("-w", "--words", type=int, help="make a passphrase of N words instead")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    a = ap.parse_args(argv)
    for _ in range(a.count):
        print(passphrase(a.words) if a.words else password(a.length, not a.no_symbols))
    pool = len(WORDS) if a.words else 62 + (0 if a.no_symbols else len(SYMBOLS))
    bits = entropy_bits(pool, a.words or a.length)
    print(f"# about {bits:.0f} bits of entropy each")
    return 0
