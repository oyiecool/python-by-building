# healthcheck.py - run every 5 minutes from cron/Task Scheduler
import csv, json, logging, socket, sys
from datetime import datetime
from pathlib import Path
import psutil

BASE = Path(__file__).resolve().parent
CONFIG = json.loads((BASE / "health.json").read_text()) if (BASE / "health.json").exists() else {
    "cpu_max": 85, "mem_max": 90, "disk_max": 90, "disk_path": "/",
    "services": [["localhost", 22], ["localhost", 80]],
}
HISTORY = BASE / "health_history.csv"
logging.basicConfig(filename=BASE / "health.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False

def collect() -> dict:
    return {
        "time": datetime.now().isoformat(timespec="seconds"),
        "host": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "mem": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage(CONFIG["disk_path"]).percent,
        "down": ";".join(f"{h}:{p}" for h, p in CONFIG["services"] if not port_open(h, p)),
    }

def problems(m: dict) -> list[str]:
    out = []
    for key in ("cpu", "mem", "disk"):
        if m[key] > CONFIG[f"{key}_max"]:
            out.append(f"{key.upper()} at {m[key]}% (limit {CONFIG[key + '_max']}%)")
    if m["down"]:
        out.append(f"services down: {m['down']}")
    return out

def record(m: dict):
    new = not HISTORY.exists()
    with HISTORY.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(m))
        if new:
            w.writeheader()
        w.writerow(m)

if __name__ == "__main__":
    m = collect()
    record(m)
    issues = problems(m)
    if issues:
        logging.warning("%s: %s", m["host"], "; ".join(issues))
        print("ALERT:", *issues, sep="\n  ")
        # send_alert(f"[{m['host']}] health alert", "\n".join(issues))  # from 13.6
        sys.exit(2)
    logging.info("OK cpu=%s mem=%s disk=%s", m["cpu"], m["mem"], m["disk"])
