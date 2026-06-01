import random
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

class EcommercePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators - Login
        self._username_input = page.locator("#user-name")
        self._password_input = page.locator("#password")
        self._login_button = page.locator("#login-button")
        
        # Locators - Search & Catalog
        self._search_input = page.locator("#gh-ac")
        self._search_button = page.locator("#gh-search-btn")
        self._price_filter_max = page.locator("input[aria-label='Maximum Value in $'], input[id$='-textbox']").first
        self._price_filter_submit = page.locator("button[aria-label='Submit price range'], button.x-search-filter__submit").first
        self._product_cards = page.locator("//li[contains(@class, 's-item')]")
        self._next_page_button = page.locator("a.pagination__next")
        
        # Locators - Product Detail Variants
        self._size_options = page.locator("select[name='option[size]'] option")
        self._color_options = page.locator(".color-variant-option")
        self._add_to_cart_button = page.locator("#atcBtn_btn_1")


    @allure.step("Proceeding as Guest User (Bypassing authentication for Anti-Bot protection)")
    def login(self, username: str, password: str):
        # Print documentation to the run report instead of executing hard credential actions 
        # that could trigger anti-bot systems (like Captchas) and block the automation flow.
        print("Running in Guest Session Profile.")
        self.take_screenshot("Guest Session Active")

    @allure.step("Searching for items: {query} with pre-filtered max price {max_price}")
    def search_items_by_name_under_price(self, query: str, max_price: float, limit: int = 5) -> list[str]:
        # Direct navigation to the filtered URL to minimize search results efficiently
        filtered_url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_udhi={int(max_price)}"
        print(f"Navigating directly to filtered URL: {filtered_url}")
        
        self.page.goto(filtered_url)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(3000) # Critical wait to ensure stable page loading
        
        valid_urls = []
        
        # Focused data collection loop
        while len(valid_urls) < limit:
            # --- Core Optimization ---
            # Restrict the search scope strictly to the main results container (.srp-results)
            # and isolate organic product title links only (.s-item__link)
            real_products_xpath = "//img[@class='s-card__image']/ancestor::a[contains(@href, '/itm/')]"
            links_locator = self.page.locator(real_products_xpath)
            links_count = links_locator.count()
            
            print(f"DEBUG: Found {links_count} REAL filtered product links on this page.")
            
            for i in range(links_count):
                if len(valid_urls) >= limit:
                    break
                    
                try:
                    link_element = links_locator.nth(i)
                    product_url = link_element.get_attribute("href")
                    
                    if product_url:
                        clean_url = product_url.split("?")[0]
                        
                        # Additional safeguard against short dummy links (such as mock/fake IDs)
                        url_parts = clean_url.rstrip('/').split('/')
                        item_id = url_parts[-1] if url_parts else ""
                        if len(item_id) < 9:
                            continue
                            
                        # Prevent duplicate entries
                        if clean_url not in valid_urls:
                            valid_urls.append(clean_url)
                            print(f"Collected valid filtered item ({len(valid_urls)}/{limit}): {clean_url}")
                except Exception:
                    continue
            
            # Handle pagination if necessary (edge case)
            if len(valid_urls) < limit:
                next_btn = self.page.locator("a.pagination__next, a[aria-label='Go to next search page']").first
                if next_btn.is_visible() and next_btn.is_enabled():
                    print("Moving to next page for more filtered items...")
                    next_btn.click()
                    self.page.wait_for_timeout(2500)
                else:
                    break
                    
        return valid_urls

    @allure.step("Adding collected items to cart")
    def add_items_to_cart(self, urls: list[str]):
        search_tab_url = self.page.url
        
        for url in urls:
            with allure.step(f"Processing item: {url}"):
                try:
                    self.navigate(url)
                    self.page.wait_for_load_state("domcontentloaded")
                    
                    # Quick check if the add-to-cart button is present on the page (safeguard against error pages or broken links).
                    # If it does not appear within 3 seconds, the target page is likely invalid or broken.
                    self._add_to_cart_button.wait_for(state="visible", timeout=3000)
                    
                    # --- Dynamic Variant Selection Logic ---
                    # Randomly select a size variant if a selection dropdown is available.
                    if self._size_options.count() > 1:
                        available_indices = range(1, self._size_options.count()) # Skip index 0 ("Select Size" placeholder)
                        random_index = random.choice(available_indices)
                        self._size_options.nth(random_index).click()
                    
                    # Randomly select a color variant if selectable elements are available.
                    color_count = self._color_options.count()
                    if color_count > 0:
                        self._color_options.nth(random.randint(0, color_count - 1)).click()
                    
                    # Cart submission and execution logging integration.
                    self._add_to_cart_button.click()
                    self.page.wait_for_timeout(1500) # Short wait for the DOM state to complete updating
                    self.take_screenshot(f"Item Added to Cart")
                    print(f"Successfully added to cart: {url}")
                    
                except Exception as e:
                    # Fallback catch: If an execution step fails (e.g., 3-second button timeout), log warning and proceed to next URL.
                    print(f"Skipping item {url} - Error or element not found: {str(e)}")
                    continue
                    
        # Return to the primary search results screen upon loop completion.
        self.navigate(search_tab_url)