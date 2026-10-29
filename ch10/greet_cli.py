# greet_cli.py
import argparse
parser = argparse.ArgumentParser(description="Greet someone")
parser.add_argument("name")
parser.add_argument("-n", "--times", type=int, default=1, help="repeat count")
parser.add_argument("--shout", action="store_true")
args = parser.parse_args()
msg = f"Hello, {args.name}!"
for _ in range(args.times):
    print(msg.upper() if args.shout else msg)
