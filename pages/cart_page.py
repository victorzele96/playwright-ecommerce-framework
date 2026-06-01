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
        # Avoid flakey icon clicks that might be hidden or dynamic; navigate directly to the cart URL instead.
        self.navigate("https://cart.ebay.com")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000) # A short wait for the prices to update in the DOM
        
        # Parse price
        try:
            total_text = self._total_price_label.text_content()
            actual_total = self.parse_price(total_text)
        except Exception:
            # פתרון גיבוי למקרה שהסלקטור דינמי - שולפים כל טקסט שמייצג סכום סופי
            total_text = self.page.locator(".app-subtotal-stack").text_content()
            actual_total = self.parse_price(total_text)
            
        # Calculate price limit
        allowed_threshold = budget_per_item * items_count
        
        # Screenshot Allure
        self.take_screenshot("Cart Review Stage")
        
        # Assertion
        with allure.step(f"Validating: Actual Total ({actual_total}) <= Allowed Threshold ({allowed_threshold})"):
            assert actual_total <= allowed_threshold, \
                f"Budget Exceeded! Total cart cost is {actual_total}, but maximum allowed threshold was {allowed_threshold}."