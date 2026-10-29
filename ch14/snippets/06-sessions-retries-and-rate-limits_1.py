import time, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.headers.update({"User-Agent": "python-by-building/1.0"})
retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry))

for page in range(1, 4):
    r = session.get("https://api.github.com/repos/python/cpython/issues",
                    params={"page": page, "per_page": 5}, timeout=10)
    print(page, r.status_code, r.headers.get("X-RateLimit-Remaining"))
    time.sleep(1)          # be polite
