from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)      # headless=False to watch it work
    page = browser.new_page()
    page.goto("http://127.0.0.1:8099/index.html")
    page.wait_for_selector(".price")                # wait for JavaScript to fill the list
    for item in page.locator(".item").all():
        print(item.inner_text())
    page.get_by_role("link", name="Log in").click()
    page.get_by_label("User").fill("demo")
    page.get_by_label("Password").fill("not-a-real-password")
    page.get_by_role("button", name="Sign in").click()
    expect(page.locator("#msg")).to_have_text("Welcome, demo!")
    print(page.locator("#msg").inner_text())
    page.screenshot(path="after_login.png")
    browser.close()
