# netscan.py - Capstone 6
"""Inventory a subnet you administer: live hosts, names, open service ports. Saves CSV."""
import argparse
import csv
import ipaddress
import platform
import socket
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

PORTS = {22: "ssh", 53: "dns", 80: "http", 139: "netbios", 443: "https", 445: "smb",
         3306: "mysql", 3389: "rdp", 5432: "postgres", 8080: "http-alt", 9100: "printer"}


def ping(ip: str, timeout_s: int = 1) -> bool:
    if platform.system() == "Windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout_s * 1000), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout_s), ip]
    try:
        return subprocess.run(cmd, capture_output=True, timeout=timeout_s + 2).returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def port_open(ip: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False


def hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except OSError:
        return ""


def probe(ip: str) -> dict | None:
    t0 = time.perf_counter()
    open_ports = [p for p in PORTS if port_open(ip, p)]
    alive = bool(open_ports) or ping(ip)       # some hosts block ping but serve ports, or the reverse
    if not alive:
        return None
    return {"ip": ip, "hostname": hostname(ip),
            "open_ports": " ".join(f"{p}/{PORTS[p]}" for p in open_ports),
            "guess": guess_role(open_ports),
            "probe_ms": round((time.perf_counter() - t0) * 1000)}


def guess_role(ports: list[int]) -> str:
    if 9100 in ports:
        return "printer"
    if 3389 in ports or 445 in ports:
        return "windows host"
    if {3306, 5432} & set(ports):
        return "database server"
    if {80, 443, 8080} & set(ports):
        return "web server"
    if 53 in ports:
        return "dns / router"
    if 22 in ports:
        return "linux / network device"
    return "unknown"


def scan(network: str, workers: int) -> list[dict]:
    hosts = [str(h) for h in ipaddress.ip_network(network, strict=False).hosts()]
    if len(hosts) > 1024:
        raise SystemExit("Refusing to scan more than 1,024 addresses at once.")
    print(f"Scanning {len(hosts)} addresses in {network} with {workers} threads...")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = [r for r in pool.map(probe, hosts) if r]
    return sorted(results, key=lambda r: ipaddress.ip_address(r["ip"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Scan a network you are authorized to scan")
    ap.add_argument("network", help="e.g. 192.168.1.0/24")
    ap.add_argument("--workers", type=int, default=64)
    ap.add_argument("--csv", default=f"inventory_{datetime.now():%Y%m%d_%H%M}.csv")
    a = ap.parse_args()
    t0 = time.perf_counter()
    found = scan(a.network, a.workers)
    print(f"\n{'IP':<16}{'Hostname':<28}{'Role guess':<24}Open ports")
    for r in found:
        print(f"{r['ip']:<16}{r['hostname'][:26]:<28}{r['guess']:<24}{r['open_ports']}")
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ip", "hostname", "guess", "open_ports", "probe_ms"])
        w.writeheader()
        w.writerows(found)
    print(f"\n{len(found)} live hosts in {time.perf_counter() - t0:.1f} s; saved {a.csv}")
