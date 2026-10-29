"""webcheck.py - check a site's TLS certificate and security headers (only sites you run!)."""
import socket
import ssl
import sys
from datetime import datetime, timezone

import requests

WANTED = {
    "Strict-Transport-Security": "forces HTTPS on return visits",
    "Content-Security-Policy": "limits where scripts may load from (stops most XSS)",
    "X-Content-Type-Options": "stops MIME sniffing (value: nosniff)",
    "X-Frame-Options": "stops click-jacking in frames (or CSP frame-ancestors)",
    "Referrer-Policy": "limits what URLs leak to other sites",
}


def cert_info(host: str, port: int = 443, cafile: str | None = None) -> dict:
    ctx = ssl.create_default_context(cafile=cafile)      # verifies chain AND hostname
    with socket.create_connection((host, port), timeout=10) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            cert = tls.getpeercert()
            version = tls.version()
    expires = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notAfter"]), timezone.utc)
    issuer = dict(x[0] for x in cert["issuer"]).get("organizationName", "?")
    return {"host": host, "tls": version, "issuer": issuer, "expires": expires.date(),
            "days_left": (expires - datetime.now(timezone.utc)).days}


def header_gaps(url: str, verify=True) -> list[str]:
    r = requests.get(url, timeout=10, verify=verify)
    return [f"{h}: {why}" for h, why in WANTED.items() if h not in r.headers]


if __name__ == "__main__":
    for host in sys.argv[1:]:
        try:
            c = cert_info(host)
        except (ssl.SSLError, OSError) as e:                # expired, wrong name, unreachable...
            print(f"{host}: TLS problem: {e}")
            continue
        flag = "RENEW NOW" if c["days_left"] < 14 else "renew soon" if c["days_left"] < 30 else "ok"
        print(f"{host}: {c['tls']}, issuer {c['issuer']}, expires {c['expires']} "
              f"({c['days_left']} days) {flag}")
        for gap in header_gaps(f"https://{host}/"):
            print(f"    missing {gap}")
