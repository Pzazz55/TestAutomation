from time import sleep
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.demoblaze.com/index.html"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context =  browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    context.tracing.stop(path="../reports/trace.zip")
    page.close()

def test_login(page):
    page.goto(BASE_URL)
    sleep(5)

    elements = page.locator('a').all()
    print("\n ##### Below are the list of Elements #####")
    for e in elements:
        print(e.text_content())

    page.wait_for_selector("//div[@id='tbodyid']//h4//a")
    products = page.locator("//div[@id='tbodyid']//h4//a").all()
    print("\n ##### Below are the list of Products #####")
    for p in products:
        print(p.text_content())

if __name__ == "__main__":
    test_login(page)