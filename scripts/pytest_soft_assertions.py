'''
Hard Assertion - If the Assertion fails, the rest of the code will not work - terminate the code.
Soft Assertion - If the Assertion fails, the rest of the code will still work.
'''

import asyncio
import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
async def test_soft_assertions():
    soft_assertions = []  # List to store failed assertions

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=False)
        page = await browser.new_page()
        await page.goto("https://demo.nopcommerce.com/register")

        # Soft Assertion Function
        async def soft_expect(async_assertion, message):
            try:
                await async_assertion
            except AssertionError as e:
                soft_assertions.append(f"{message}: {str(e)}")

        # 1. Soft assertion for the 'URL'
        await soft_expect(
            expect(page).to_have_url("https://demoi.nopcommerce.com/register"),"URL mismatch"
        )

        # 2. Soft assertion for the 'title'
        await soft_expect(
            expect(page).to_have_title("nopCommerce demo store. some random value Register"),"Title mismatch"
        )

        # 3. Soft assertion for the 'logo' visibility
        logoElement = page.locator('.header-logo')
        await soft_expect(
            expect(logoElement).to_be_visible(),"Logo is not visible"
        )

        await browser.close()

        # Raise collected assertion failures at the end
        if soft_assertions:
            raise AssertionError("\n".join(soft_assertions))

        # pytest .\scripts\pytest_soft_assertions.py --html=reports/test_report.html