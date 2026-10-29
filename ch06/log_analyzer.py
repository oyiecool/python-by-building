# log_analyzer.py
import re
from collections import Counter

LINE = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\w+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\d+|-)'
)

SAMPLE = """\
10.0.0.5 - - [29/Oct/2026:10:00:01] "GET / HTTP/1.1" 200 5120
10.0.0.7 - - [29/Oct/2026:10:00:03] "GET /login HTTP/1.1" 200 2311
10.0.0.5 - - [29/Oct/2026:10:00:09] "POST /login HTTP/1.1" 302 0
10.0.0.9 - - [29/Oct/2026:10:01:11] "GET /admin HTTP/1.1" 403 199
10.0.0.9 - - [29/Oct/2026:10:01:12] "GET /admin HTTP/1.1" 403 199
10.0.0.7 - - [29/Oct/2026:10:02:40] "GET /missing HTTP/1.1" 404 150
10.0.0.5 - - [29/Oct/2026:10:03:00] "GET /api/items HTTP/1.1" 500 87
"""

def analyze(lines):
    statuses, paths, ips = Counter(), Counter(), Counter()
    total_bytes = bad = 0
    for line in lines:
        m = LINE.match(line)
        if not m:
            bad += 1
            continue
        statuses[m["status"]] += 1
        paths[m["path"]] += 1
        ips[m["ip"]] += 1
        if m["size"] != "-":
            total_bytes += int(m["size"])
    return statuses, paths, ips, total_bytes, bad

def report(lines):
    statuses, paths, ips, total_bytes, bad = analyze(lines)
    total = sum(statuses.values())
    print(f"Requests: {total}   Bytes: {total_bytes:,}   Unparsed: {bad}")
    print("\nStatus codes:")
    for code, n in sorted(statuses.items()):
        bar = "#" * n
        print(f"  {code}  {n:>4}  {bar}")
    errors = sum(n for c, n in statuses.items() if c.startswith(("4", "5")))
    print(f"  Error rate: {errors / total:.1%}")
    print("\nTop pages:")
    for path, n in paths.most_common(5):
        print(f"  {n:>4}  {path}")
    print("\nTop clients:")
    for ip, n in ips.most_common(3):
        print(f"  {n:>4}  {ip}")

if __name__ == "__main__":
    report(SAMPLE.splitlines())
