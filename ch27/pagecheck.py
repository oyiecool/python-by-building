# pagecheck.py - Chapter 27 mini project
"""Open pages in a real (headless) browser: load time, console errors, broken images,
broken links and a full-page screenshot for each. Results go to a CSV report."""
import argparse
import csv
import time
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


def check_page(page, url: str, shots: Path) -> dict:
    errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("requestfailed", lambda r: failed.append(r.url))
    t0 = time.perf_counter()
    resp = page.goto(url, wait_until="networkidle", timeout=30_000)
    load_ms = round((time.perf_counter() - t0) * 1000)
    broken_imgs = page.eval_on_selector_all(
        "img", "imgs => imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.src)")
    links = {urljoin(url, h) for h in page.eval_on_selector_all("a[href]", "as => as.map(a => a.getAttribute('href'))")
             if not h.startswith(("mailto:", "#", "javascript:"))}
    bad_links = []
    for link in sorted(links):
        r = page.request.get(link, fail_on_status_code=False)
        if r.status >= 400:
            bad_links.append(f"{link} ({r.status})")
    shot = shots / (url.rstrip("/").split("/")[-1].replace(".", "_") or "home")
    page.screenshot(path=f"{shot}.png", full_page=True)
    return {"url": url, "status": resp.status if resp else 0, "title": page.title(), "load_ms": load_ms,
            "console_errors": len(errors), "broken_images": len(broken_imgs), "broken_links": len(bad_links),
            "details": "; ".join(errors + broken_imgs + bad_links)[:300]}


def main(urls: list[str], out: Path) -> None:
    shots = out.parent / "screenshots"
    shots.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        results = []
        for url in urls:
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            try:
                results.append(check_page(page, url, shots))
            except Exception as e:                       # one bad page must not stop the run
                results.append({"url": url, "status": 0, "title": "", "load_ms": 0, "console_errors": 0,
                                "broken_images": 0, "broken_links": 0, "details": f"FAILED: {e}"[:300]})
            page.close()
        browser.close()
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    for r in results:
        flag = "OK  " if not (r["console_errors"] or r["broken_images"] or r["broken_links"]) else "WARN"
        print(f"{flag} {r['status']} {r['load_ms']:>5} ms  {r['title'][:28]:<30}{r['url']}")
        if r["details"]:
            print(f"      {r['details']}")
    print(f"\nReport: {out}   Screenshots: {shots}/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--out", type=Path, default=Path("pagecheck.csv"))
    a = ap.parse_args()
    main(a.urls, a.out)
