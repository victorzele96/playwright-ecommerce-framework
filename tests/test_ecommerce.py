import json
import os
import allure
import pytest
from playwright.sync_api import Page, sync_playwright
from pages.ecommerce_page import EcommercePage
from pages.cart_page import CartPage

def load_config():
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, '../data/config.json')
    with open(config_path, 'r') as file:
        return json.load(file)

# אנחנו מגדירים Fixture מותאם אישית שמחביא את סימני האוטומציה
@pytest.fixture
def human_page():
    with sync_playwright() as p:
        # הפעלת הדפדפן עם הגדרות שמחקות דפדפן רגיל של משתמש
        browser = p.chromium.launch(
            headless=False, # משאיר דפדפן פתוח ויזואלית
            args=["--disable-blink-features=AutomationControlled"] # מוחק את ה-Flag של האוטומציה מה-DOM
        )
        
        # יצירת קונטקסט עם יוזר אייג'נט של כרום רגיל לחלוטין ומסך סטנדרטי
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        yield page
        
        context.close()
        browser.close()

@allure.epic("E-Commerce Automation Framework")
@allure.feature("Cart Budget Enforcement")
def test_budget_enforcement_flow(human_page): # משתמשים ב-Fixture האנושי שלנו
    config = load_config()
    ecommerce = EcommercePage(human_page)
    cart = CartPage(human_page)
    
    # 1. Login ( as Guest further explanation in README).
    ecommerce.navigate(config["target_url"])
    ecommerce.login("guest", "guest")
    
    # 2. חיפוש תחת תנאי מחיר עם מגבלת כמות ו-Paging
    product_urls = ecommerce.search_items_by_name_under_price(
        query=config["search_query"], 
        max_price=config["max_price"], 
        limit=config["limit"]
    )
    
    # 3. Adding choosen items into cart.
    ecommerce.add_items_to_cart(product_urls)
    
    # 4. Assert cart price.
    cart.assert_cart_total_not_exceeds(
        budget_per_item=config["max_price"], 
        items_count=len(product_urls)
    )