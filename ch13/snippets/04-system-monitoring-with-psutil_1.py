import psutil, platform
from datetime import datetime

print("CPU %:", psutil.cpu_percent(interval=1))
print("Per core:", psutil.cpu_percent(interval=1, percpu=True))
mem = psutil.virtual_memory()
print(f"RAM: {mem.percent}% of {mem.total / 2**30:.1f} GiB")
for part in psutil.disk_partitions():
    try:
        u = psutil.disk_usage(part.mountpoint)
        print(f"{part.mountpoint:<12}{u.percent:>5}% used of {u.total / 2**30:.0f} GiB")
    except PermissionError:
        pass
boot = datetime.fromtimestamp(psutil.boot_time())
print("Up since:", boot)

top = sorted(psutil.process_iter(["pid", "name", "memory_percent"]),
             key=lambda p: p.info["memory_percent"] or 0, reverse=True)[:5]
for p in top:
    print(f"{p.info['pid']:>7} {p.info['name']:<25}{p.info['memory_percent']:.1f}%")
