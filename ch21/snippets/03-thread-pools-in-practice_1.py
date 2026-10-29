from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

urls = ["https://www.python.org", "https://pypi.org", "https://github.com"]

def fetch(url):
    r = requests.get(url, timeout=10)
    return url, r.status_code, len(r.content)

with ThreadPoolExecutor(max_workers=10) as pool:
    futures = {pool.submit(fetch, u): u for u in urls}
    for fut in as_completed(futures):
        try:
            url, status, size = fut.result()
            print(f"{status} {size:>9,} bytes  {url}")
        except requests.RequestException as e:
            print("failed:", futures[fut], e)
