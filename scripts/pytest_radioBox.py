'''
page.locator().check()
expect(page.locator()).toBeChecked()
expect(page.locator().isChecked()).toBeTruthy()
expect(page.locator().isChecked()).toBeFalsy()
'''

import asyncio
import pytest
from playwright.async_api import async_playwright, expect
from time import sleep

@pytest.mark.asyncio
async def test_assertions():
    async with async_playwright() as p:

        #Global Timeout
        expect.set_options(timeout=10_000)

        browser = await p.chromium.launch(channel="chrome", headless=False)
        page = await browser.new_page()
        await page.goto("https://www.w3schools.com/howto/howto_css_custom_checkbox.asp")
        await page.wait_for_timeout(5000)

        # <input type="radio" value="M" id="gender-male" name= Gender" xpath="1">
        await expect(page.locator("//label[normalize-space()='First']//span[@class='checkmark']")).to_be_visible()
        await expect(page.locator("//label[normalize-space()='Second']//span[@class='checkmark']")).to_be_visible()
        await expect(page.locator("//label[normalize-space()='Third']//span[@class='checkmark']")).to_be_visible()
        await expect(page.locator("//label[normalize-space()='Four']//span[@class='checkmark']")).to_be_visible()
        await page.wait_for_timeout(5000)

        await expect(page.locator("//label[normalize-space()='First']//span[@class='checkmark']")).not_to_be_checked() #checks if the checkbox is not checked
        await expect(page.locator("//label[normalize-space()='Second']//span[@class='checkmark']")).to_be_checked() #checks if the checkbox is not checked
        await expect(page.locator("//label[normalize-space()='Third']//span[@class='checkmark']")).to_be_checked() #checks if the checkbox is not checked
        await expect(page.locator("//label[normalize-space()='Four']//span[@class='checkmark']")).to_be_checked() #checks if the checkbox is not checked
        await page.wait_for_timeout(5000)

        await page.locator("//label[normalize-space()='Second']//span[@class='checkmark']").click()
        await page.locator("//label[normalize-space()='Third']//span[@class='checkmark']").click()
        await page.wait_for_timeout(5000)

        await expect(page.locator("//label[normalize-space()='First']//span[@class='checkmark']")).not_to_be_checked() #checks if the checkbox is not checked
        await expect(page.locator("//label[normalize-space()='Second']//span[@class='checkmark']")).not_to_be_checked() #checks if the checkbox is not checked
        await expect(page.locator("//label[normalize-space()='Third']//span[@class='checkmark']")).not_to_be_checked() #checks if the checkbox is not checked
        await expect(page.locator("//label[normalize-space()='Four']//span[@class='checkmark']")).to_be_checked() #checks if the checkbox is not checked
        await page.wait_for_timeout(5000)

        await page.locator("//label[normalize-space()='Second']//span[@class='checkmark']").click()
        await expect(page.locator("//label[normalize-space()='Second']//span[@class='checkmark']")).to_be_checked() #checks if the checkbox is not checked
        await page.wait_for_timeout(5000) #pausing the code for 5 seconds

        await browser.close()

# pytest .\scripts\pytest_radioBox.py --html=reports/test_report.html