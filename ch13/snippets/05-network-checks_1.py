import socket, subprocess, sys

def port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

def ping(host: str) -> bool:
    flag = "-n" if sys.platform == "win32" else "-c"
    r = subprocess.run(["ping", flag, "1", host], capture_output=True)
    return r.returncode == 0

print(socket.gethostbyname("python.org"))
for host, port in [("python.org", 443), ("localhost", 22), ("8.8.8.8", 53)]:
    print(f"{host}:{port} ->", "open" if port_open(host, port) else "closed")
