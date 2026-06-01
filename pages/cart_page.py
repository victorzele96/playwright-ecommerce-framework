import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._cart_icon_link = page.locator(".gh-cart__icon")
        self._total_price_label = page.locator("[data-test-id='SUBTOTAL'], .app-subtotal-stack__item-amount").first

    @allure.step("Asserting cart total does not exceed budget threshold")
    def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int):
        # במקום ללחוץ על האייקון ולהסתכן בזה שהוא מוסתר או השתנה - ניגשים ישירות ל-URL של העגלה!
        self.navigate("https://cart.ebay.com")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000) # המתנה קלה שהמחירים יתעדכנו ב-DOM
        
        # קריאת טקסט המחיר מהאתר
        try:
            total_text = self._total_price_label.text_content()
            actual_total = self.parse_price(total_text)
        except Exception:
            # פתרון גיבוי למקרה שהסלקטור דינמי - שולפים כל טקסט שמייצג סכום סופי
            total_text = self.page.locator(".app-subtotal-stack").text_content()
            actual_total = self.parse_price(total_text)
            
        # חישוב תקרת התקציב המותרת
        allowed_threshold = budget_per_item * items_count
        
        # צילום מסך של העגלה לדו"ח Allure
        self.take_screenshot("Cart Review Stage")
        
        # ביצוע ה-Assertion
        with allure.step(f"Validating: Actual Total ({actual_total}) <= Allowed Threshold ({allowed_threshold})"):
            assert actual_total <= allowed_threshold, \
                f"Budget Exceeded! Total cart cost is {actual_total}, but maximum allowed threshold was {allowed_threshold}."