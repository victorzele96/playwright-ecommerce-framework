import re
import allure
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def take_screenshot(self, description: str):
        """Takes a screenshot and automatically attaches it to the Allure report."""
        screenshot_bytes = self.page.screenshot()
        allure.attach(
            screenshot_bytes, 
            name=description, 
            attachment_type=allure.attachment_type.PNG
        )

    def parse_price(self, price_text: str) -> float:
        """Cleans currency symbols ($, ₪) and converts the value to a float for price validation."""
        if not price_text:
            return 0.0
        # Extract only numbers and decimal points using Regex
        clean_price = re.sub(r'[^\d.]', '', price_text)
        return float(clean_price) if clean_price else 0.0