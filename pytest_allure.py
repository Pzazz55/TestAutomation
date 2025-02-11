import asyncio
import pytest
import logging
import allure
from playwright.async_api import async_playwright

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@pytest.mark.asyncio
@allure.feature("OrangeHRM Login Test")
@allure.story("Login functionality verification")
async def test_orangehrm_login(caplog):
    caplog.set_level(logging.INFO)  # Capture pytest logs

    async with async_playwright() as p:
        # Launching the browser
        with allure.step("Launch Browser and Open Login Page"):
            logger.info("Launching browser...")
            browser = await p.chromium.launch(channel="chrome", headless=False)
            page = await browser.new_page()
            await page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
            await page.wait_for_load_state("domcontentloaded")  # Wait for the page to load

        try:
            # 1. Assertion for 'Company Logo' visibility
            with allure.step("Check if company branding logo is visible"):
                logger.info("Checking if company logo is visible on the login page")
                company_logo = page.locator('img[alt="company-branding"]')
                await company_logo.wait_for(state="visible")  # Ensure it's visible before assertion
                assert await company_logo.is_visible()

            # 2. Fill 'Username' and 'Password' fields
            with allure.step("Fill in Username and Password fields"):
                logger.info("Filling in username and password")
                await page.fill('input[placeholder="Username"]', 'Admin')
                await page.fill('input[placeholder="Password"]', 'admin123')

            # 3. Click on 'Login' button
            with allure.step("Click on Login button"):
                logger.info("Clicking on Login button")
                await page.click('button[type="submit"]')
                await page.wait_for_load_state("networkidle")  # Wait for the network to be idle after login

            # 4. Assertion for 'User Dropdown Name' visibility after login
            with allure.step("Check if user dropdown name is visible after login"):
                logger.info("Checking if user dropdown name is visible")
                user_dropdown_name = page.locator('//p[@class="oxd-userdropdown-name"]')
                await user_dropdown_name.wait_for(state="visible")  # Ensure it's visible before assertion
                assert await user_dropdown_name.is_visible()

            # 5. Verify login name appears correctly in the page
            with allure.step("Verify login name is displayed"):
                logger.info("Extracting login name text and verifying")
                login_name = await user_dropdown_name.text_content()
                assert login_name and await page.locator(f'//*[text()="{login_name}"]').is_visible()

        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

        finally:
            # 6. Closing the browser (done last to ensure all actions complete)
            with allure.step("Closing the browser"):
                logger.info("Closing the browser after test execution")
                await browser.close()

    # Capture logs and attach them to Allure report
    with allure.step("Attach logs to the report"):
        allure.attach("\n".join([record.message for record in caplog.records]),
                      name="Test Logs",
                      attachment_type=allure.attachment_type.TEXT)

    # Print captured logs
    for record in caplog.records:
        print(f"{record.levelname}: {record.message}")

# pytest .\scripts\pytest_allure.py --alluredir=allure-results
# pytest .\scripts\pytest_allure.py --html=reports/test_report.html --self-contained-html --alluredir=allure-results