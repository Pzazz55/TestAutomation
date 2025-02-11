import asyncio
import pytest
from playwright.async_api import async_playwright
from time import sleep

@pytest.mark.asyncio
async def test_orangehrm_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=False)
        page = await browser.new_page()
        await page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        sleep(2)

        assert await page.get_by_alt_text('company-branding').is_visible()
        await page.get_by_placeholder('Username').fill('Admin')
        await page.get_by_placeholder('Password').fill('admin123')
        await page.get_by_role("button", name="Login").click()
        sleep(2)

        await page.locator('//p[@class="oxd-userdropdown-name"]').is_visible()
        login_name = await page.locator('//p[@class="oxd-userdropdown-name"]').text_content()
        assert await page.get_by_text(login_name).is_visible()

        await browser.close()