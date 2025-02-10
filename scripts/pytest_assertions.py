'''
1) expect(page).toHaveURL()   Page has URL
2) expect(page).toHaveTitle()   Page has title
3) expect(locator).toBeVisible()  Element is visible
4) expect(locator).toBeEnabled()  Control is enabled
5) expect(locator).toBeChecked()  Radio/Checkbox is checked
6) expect(locator).toHaveAttribute() Element has attribute
7) expect(locator).toHaveText()  Element matches text
8) expect(locator).toContainText()  Element contains text
9) expect(locator).toHaveValue(value) Input has a value
10) expect(locator).toHaveCount()  List of elements has given length
'''

import asyncio
import pytest
from playwright.async_api import async_playwright, expect
from time import sleep

@pytest.mark.asyncio
async def test_assertions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=False)
        page = await browser.new_page()
        await page.goto("https://demo.nopcommerce.com/register")

        # 1. Assertion for the 'URL' - expect().to_have_url()
        await expect(page).to_have_url("https://demo.nopcommerce.com/register")

        # 2. Assertion for the 'title' - expect().to_have_title()
        await expect(page).to_have_title("nopCommerce demo store. Register")

        # 3. Assertion for the 'logo' - expect().to_be_visible()
        logoElement = page.locator('.header-logo')
        await expect(logoElement).to_be_visible()

        # 4. Assertion for the 'search store' - expect().to_be_enabled()
        searchStore = page.locator('#small-searchterms')
        await expect(searchStore).to_be_enabled()

        # 5. Assertion for the 'radio button' & 'checkbox' - expect().to_be_checked()
        genderRadio = page.locator('#gender-male')
        await genderRadio.click()
        await expect(genderRadio).to_be_checked()

        checkBox = page.locator('#Newsletter')
        await expect(checkBox).to_be_checked()

        # 6. Assertion for the 'button' - expect().to_have_attribute()
        regButton = page.locator('#register-button')
        await expect(regButton).to_have_attribute('type','submit')

        # 7. Assertion to check the 'text' - expect().to_have_text()
        await expect(page.locator('.page-title h1')).to_have_text('Register') #full text

        # 8. Assertion to check the 'text' - expect().to_contain_text()
        await expect(page.locator('.page-title h1')).to_contain_text('Regi') #partial text

        # 9. Assertion to check the 'input value' - expect().to_have_value()
        emailInput = page.locator('#Email') #selector: the css for id value can be shown with '#'
        await emailInput.fill('test@demo.com')
        await expect(emailInput).to_have_value('test@demo.com')

        # 10. Assertion to check the 'dropdown value' - expect().to_have_value()
        dobMonth = page.locator('select[name="DateOfBirthMonth"] option')
        await expect(dobMonth).to_have_count(13)

        await browser.close()

        # pytest .\scripts\pytest_assertions.py --html=reports/test_report.html