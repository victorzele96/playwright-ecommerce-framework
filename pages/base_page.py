import re
import allure
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def take_screenshot(self, description: str):
        """מצלם מסך ומצרף אותו אוטומטית לדו''ח של Allure"""
        screenshot_bytes = self.page.screenshot()
        allure.attach(
            screenshot_bytes, 
            name=description, 
            attachment_type=allure.attachment_type.PNG
        )

    def parse_price(self, price_text: str) -> float:
        """מנקה סימני מטבע ($, ₪) וממירה מספר צף לתנאי מחיר"""
        if not price_text:
            return 0.0
        # מוציא רק מספרים ונקודה עשרונית בעזרת Regex
        clean_price = re.sub(r'[^\d.]', '', price_text)
        return float(clean_price) if clean_price else 0.0