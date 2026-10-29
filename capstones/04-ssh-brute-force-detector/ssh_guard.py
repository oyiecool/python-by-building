# ssh_guard.py - Capstone 4
"""Find SSH brute-force attempts in a Linux auth log and suggest firewall blocks."""
import argparse
import ipaddress
import random
import re
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path

FAILED = re.compile(
    r"^(?P<ts>\w{3}\s+\d+\s[\d:]{8}) \S+ sshd\[\d+\]: Failed password for "
    r"(?:invalid user )?(?P<user>\S+) from (?P<ip>[\d.]+) port \d+")
ACCEPTED = re.compile(
    r"^(?P<ts>\w{3}\s+\d+\s[\d:]{8}) \S+ sshd\[\d+\]: Accepted \w+ for "
    r"(?P<user>\S+) from (?P<ip>[\d.]+) port \d+")


def parse_time(text: str, year: int) -> datetime:
    """Syslog lines have no year: 'Oct 29 10:42:01'."""
    return datetime.strptime(f"{year} {' '.join(text.split())}", "%Y %b %d %H:%M:%S")


def make_sample(path: Path) -> None:
    random.seed(1)
    start = datetime(2026, 10, 28, 0, 0, 0)
    lines = []
    def add(t, msg):
        lines.append(f"{t:%b %d %H:%M:%S} web01 sshd[{random.randint(1000, 9999)}]: {msg}")
    for i in range(40):                                   # normal staff logins
        t = start + timedelta(minutes=random.randint(420, 1080))
        add(t, f"Accepted publickey for {random.choice(['ronald', 'ana', 'deploy'])} "
               f"from 10.0.0.{random.randint(10, 40)} port {random.randint(40000, 60000)} ssh2")
    for i in range(5):                                    # honest typos
        t = start + timedelta(minutes=random.randint(420, 1080))
        add(t, f"Failed password for ana from 10.0.0.21 port {random.randint(40000, 60000)} ssh2")
    for ip, n, users in [("203.0.113.45", 180, ["root", "admin", "oracle", "test"]),
                         ("198.51.100.7", 60, ["root", "ubuntu"]),
                         ("192.0.2.99", 25, ["root"])]:   # attackers (documentation IP ranges)
        t = start + timedelta(hours=random.randint(0, 20))
        for _ in range(n):
            t += timedelta(seconds=random.randint(1, 8))
            u = random.choice(users)
            invalid = "invalid user " if u not in ("root",) else ""
            add(t, f"Failed password for {invalid}{u} from {ip} port {random.randint(30000, 65000)} ssh2")
    add(start + timedelta(hours=21), "Accepted password for root from 192.0.2.99 port 51111 ssh2")
    lines.sort(key=lambda l: datetime.strptime("2026 " + l[:15], "%Y %b %d %H:%M:%S"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def analyze(path: Path, threshold: int, window_min: int, year: int):
    window = timedelta(minutes=window_min)
    recent = defaultdict(deque)          # ip -> times of failures inside the window
    failures = defaultdict(int)
    users_tried = defaultdict(set)
    flagged = {}                         # ip -> first time it crossed the threshold
    suspicious_logins = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if m := FAILED.match(line):
            ip, t = m["ip"], parse_time(m["ts"], year)
            failures[ip] += 1
            users_tried[ip].add(m["user"])
            q = recent[ip]
            q.append(t)
            while q and t - q[0] > window:
                q.popleft()
            if len(q) >= threshold and ip not in flagged:
                flagged[ip] = t
        elif m := ACCEPTED.match(line):
            ip = m["ip"]
            if ip in flagged:
                suspicious_logins.append((parse_time(m["ts"], year), m["user"], ip, failures.get(ip, 0)))
    return failures, users_tried, flagged, suspicious_logins


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Detect SSH brute-force attacks")
    ap.add_argument("log", nargs="?", type=Path, default=Path("auth.log"),
                    help="e.g. /var/log/auth.log (Debian/Ubuntu) or /var/log/secure (RHEL)")
    ap.add_argument("--threshold", type=int, default=10, help="failures within the window")
    ap.add_argument("--window", type=int, default=10, help="window in minutes")
    ap.add_argument("--year", type=int, default=datetime.now().year)
    ap.add_argument("--whitelist", default="10.0.0.0/8", help="comma-separated prefixes never blocked")
    a = ap.parse_args()
    if not a.log.exists():
        make_sample(a.log)
        print(f"No log found: created sample {a.log}\n")
    failures, users, flagged, logins = analyze(a.log, a.threshold, a.window, a.year)
    safe_nets = [ipaddress.ip_network(p.strip()) for p in a.whitelist.split(",")]

    def whitelisted(ip: str) -> bool:
        return any(ipaddress.ip_address(ip) in net for net in safe_nets)

    print(f"{'IP address':<16}{'Failures':>9}  {'Users tried':<28}Status")
    for ip, n in sorted(failures.items(), key=lambda kv: -kv[1]):
        status = "WHITELISTED" if whitelisted(ip) else ("ATTACK" if ip in flagged else "ok")
        tried = ", ".join(sorted(users[ip]))[:26]
        print(f"{ip:<16}{n:>9}  {tried:<28}{status}")
    if logins:
        print("\n!!! Successful logins after a brute-force attempt (investigate now):")
        for t, user, ip, n in logins:
            print(f"   {t:%Y-%m-%d %H:%M}  {user}@{ip} after {n} failures")
    to_block = [ip for ip in flagged if not whitelisted(ip)]
    if to_block:
        print("\nSuggested firewall commands (review before running):")
        for ip in to_block:
            print(f"   sudo ufw deny from {ip} to any port 22")
