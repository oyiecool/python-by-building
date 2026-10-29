import socket

def port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    with socket.socket() as s:
        s.settimeout(timeout)
        return s.connect_ex((host, port)) == 0      # 0 means the connection succeeded
