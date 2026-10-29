# uptime.py - Chapter 21 mini project
"""Check many websites at once with asyncio + aiohttp; log status and response time to CSV."""
import argparse
import asyncio
import csv
import time
from datetime import datetime
from pathlib import Path

import aiohttp

DEFAULT_SITES = ["https://www.python.org", "https://pypi.org", "https://docs.python.org/3/",
                 "https://github.com", "https://www.wikipedia.org", "https://example.com/missing-page"]


async def check(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> dict:
    async with sem:                                        # limit how many run at once
        start = time.perf_counter()
        try:
            async with session.get(url, allow_redirects=True) as resp:
                await resp.read()
                status, error = resp.status, ""
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            status, error = 0, type(e).__name__
        ms = round((time.perf_counter() - start) * 1000)
    ok = 200 <= status < 400
    return {"checked": datetime.now().isoformat(timespec="seconds"), "url": url,
            "status": status, "ms": ms, "ok": ok, "error": error}


async def check_all(urls: list[str], limit: int, timeout: float) -> list[dict]:
    sem = asyncio.Semaphore(limit)
    t = aiohttp.ClientTimeout(total=timeout)
    headers = {"User-Agent": "python-by-building-uptime/1.0"}
    async with aiohttp.ClientSession(timeout=t, headers=headers) as session:
        return await asyncio.gather(*(check(session, u, sem) for u in urls))


def save(results: list[dict], path: Path) -> None:
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        if new:
            w.writeheader()
        w.writerows(results)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Concurrent website uptime checker")
    ap.add_argument("--file", type=Path, help="text file with one URL per line")
    ap.add_argument("--limit", type=int, default=20, help="maximum checks at the same time")
    ap.add_argument("--timeout", type=float, default=10)
    ap.add_argument("--log", type=Path, default=Path("uptime_log.csv"))
    a = ap.parse_args()
    urls = [l.strip() for l in a.file.read_text().splitlines() if l.strip()] if a.file else DEFAULT_SITES
    t0 = time.perf_counter()
    results = asyncio.run(check_all(urls, a.limit, a.timeout))
    for r in sorted(results, key=lambda r: (r["ok"], -r["ms"])):
        mark = "UP  " if r["ok"] else "DOWN"
        print(f"{mark} {r['status']:>3} {r['ms']:>6} ms  {r['url']} {r['error']}")
    save(results, a.log)
    print(f"\nChecked {len(urls)} sites in {time.perf_counter() - t0:.2f} s; appended to {a.log}")
