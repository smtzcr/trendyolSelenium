from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FilterPage(BasePage):
    CATEGORY_URL = "https://www.trendyol.com/kadin-yuzuk-x-g1-c103"

    # Fiyat aralığı filtreleri
    PRICE_SECTION_TOGGLE = (By.XPATH, '//div[normalize-space(text())="Fiyat"]')
    MIN_PRICE_INPUT = (By.XPATH, '//input[@placeholder="En Az"]')
    MAX_PRICE_INPUT = (By.XPATH, '//input[@placeholder="En Çok"]')
    APPLY_BUTTON = (By.CLASS_NAME, 'fltr-srch-prc-rng-srch')

    # Cinsiyet filtresi
    GENDER_FILTER_ERKEK = (By.XPATH, '//div[normalize-space(text())="Erkek"]')

    # Ürün fiyatlarının bulunduğu alan
    PRODUCT_PRICES = (By.CLASS_NAME, "price-item")

    def go_to_category_page(self):
        self.go_to(self.CATEGORY_URL)

    def apply_price_filter(self, min_price, max_price):
        self.scroll_to_element_in_filter_panel(*self.PRICE_SECTION_TOGGLE)
        self.click(*self.PRICE_SECTION_TOGGLE)
        self.scroll_to_element_in_filter_panel(*self.MIN_PRICE_INPUT)
        self.type(*self.MIN_PRICE_INPUT, str(min_price))
        self.type(*self.MAX_PRICE_INPUT, str(max_price))
        self.click(*self.APPLY_BUTTON)

    def apply_gender_filter(self):
        gender_element = self.scroll_to_element_in_filter_panel(*self.GENDER_FILTER_ERKEK)
        if gender_element:
            gender_element.click()

    def all_prices_within_range(self, min_price, max_price):
        self.wait_until_visible(*self.PRODUCT_PRICES)
        prices = self.driver.find_elements(*self.PRODUCT_PRICES)
        for price in prices:
            text = price.text.replace("TL", "").replace(".", "").replace(",", ".").strip()
            try:
                val = float(text)
                if not (min_price <= val <= max_price):
                    return False
            except:
                continue
        return True
