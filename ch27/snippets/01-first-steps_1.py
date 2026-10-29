from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # watch it work; True runs invisibly
    page = browser.new_page()
    page.goto("https://www.python.org")
    print(page.title())
    page.screenshot(path="python_org.png", full_page=True)
    page.pdf(path="python_org.pdf")                # PDF needs headless=True in Chromium
    browser.close()
