import asyncio
import pytest
import logging
from playwright.async_api import async_playwright, expect

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@pytest.mark.asyncio
async def test_assertions(caplog):
    caplog.set_level(logging.INFO)  # Capture pytest logs

    async with async_playwright() as p:
        logger.info("Launching browser...")
        browser = await p.chromium.launch(channel="chrome", headless=False)
        page = await browser.new_page()

        logger.info("Navigating to Register Page")
        await page.goto("https://demo.nopcommerce.com/register")

        # 1. Assertion for 'URL'
        logger.info("Checking if URL is correct")
        await expect(page).to_have_url("https://demo.nopcommerce.com/register")

        # 2. Assertion for 'Title'
        logger.info("Checking if page title is correct")
        await expect(page).to_have_title("nopCommerce demo store. Register")

        # 3. Assertion for 'Logo Visibility'
        logger.info("Checking if logo is visible")
        logoElement = page.locator('.header-logo')
        await expect(logoElement).to_be_visible()

        # 4. Assertion for 'Search Store' input field
        logger.info("Checking if search store input is enabled")
        searchStore = page.locator('#small-searchterms')
        await expect(searchStore).to_be_enabled()

        # 5. Assertion for 'Radio Button' & 'Checkbox'
        logger.info("Selecting Gender Male radio button")
        genderRadio = page.locator('#gender-male')
        await genderRadio.click()
        await expect(genderRadio).to_be_checked()

        logger.info("Checking if Newsletter checkbox is checked by default")
        checkBox = page.locator('#Newsletter')
        await expect(checkBox).to_be_checked()

        # 6. Assertion for 'Register Button' Attribute
        logger.info("Checking if Register button has correct attribute")
        regButton = page.locator('#register-button')
        await expect(regButton).to_have_attribute('type', 'submit')

        # 7. Assertion to check the 'Text Content'
        logger.info("Checking if page title text is correct")
        await expect(page.locator('.page-title h1')).to_have_text('Register')

        # 8. Assertion for Partial Text
        logger.info("Checking if title contains partial text")
        await expect(page.locator('.page-title h1')).to_contain_text('Regi')

        # 9. Assertion to check 'Input Field Value'
        logger.info("Entering email and verifying value")
        emailInput = page.locator('#Email')
        await emailInput.fill('test@demo.com')
        await expect(emailInput).to_have_value('test@demo.com')

        # 10. Assertion to check 'Dropdown Count'
        logger.info("Checking if dropdown has correct number of options")
        dobMonth = page.locator('select[name="DateOfBirthMonth"] option')
        await expect(dobMonth).to_have_count(13)

        logger.info("Closing browser")
        await browser.close()

    # Print captured logs in CLI
    for record in caplog.records:
        print(f"{record.levelname}: {record.message}")
