import subprocess, sys
cmd = ["ping", "-n" if sys.platform == "win32" else "-c", "2", "8.8.8.8"]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
print(result.returncode)
print(result.stdout[-200:])
