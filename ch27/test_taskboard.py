# test_taskboard.py  (pip install pytest-playwright; run the Chapter 15 app first)
from playwright.sync_api import Page, expect

def test_add_task(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_placeholder("New task").fill("Renew SSL certificate")
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_text("Added: Renew SSL certificate")).to_be_visible()
