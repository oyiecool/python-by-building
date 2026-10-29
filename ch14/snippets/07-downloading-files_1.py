import requests
from pathlib import Path

def download(url: str, dest: Path):
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                f.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r{done / total:6.1%}", end="")
    print("\nSaved", dest)

download("https://www.python.org/static/img/python-logo.png", Path("python-logo.png"))
