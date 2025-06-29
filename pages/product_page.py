import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    FIRST_PRODUCT = (By.CLASS_NAME, "p-card-wrppr")  # İlk ürün kutusu
    ACCEPT_BUTTON = (By.CLASS_NAME, "onboarding-popover__default-renderer-primary-button")
    PRODUCT_TITLE = (By.CLASS_NAME, "pr-new-br")        # Ürün başlığı
    PRODUCT_PRICE = (By.CLASS_NAME, "prc-dsc")          # Ürün fiyatı
    DISCOUNTED_PRICE = (By.CLASS_NAME, "campaign-price-container")
    ADD_TO_CART = (By.CLASS_NAME, "add-to-basket")      # Sepete Ekle butonu
    FAVORITE_BUTTON = (By.CLASS_NAME, "fv")

    def click_first_product(self):
        self.wait_until_visible(*self.FIRST_PRODUCT).click()
        time.sleep(3)
        self.switch_to_new_tab()
        self.wait_until_visible(*self.ACCEPT_BUTTON).click()

    def is_product_title_visible(self):
        return self.wait_until_visible(*self.PRODUCT_TITLE).is_displayed()

    def is_product_price_visible(self):
        try:
            element = self.wait_until_visible(*self.PRODUCT_PRICE, timeout=5)
            return element.is_displayed()
        except:
            try:
                discounted = self.wait_until_visible(*self.DISCOUNTED_PRICE, timeout=5)
                return discounted.is_displayed()
            except:
                return False

    def is_add_to_cart_visible(self):
        return self.wait_until_visible(*self.ADD_TO_CART).is_displayed()

    def add_to_cart(self):
        self.wait_until_visible(*self.ADD_TO_CART).click()

    def add_to_favorites(self):
        fav_button = self.wait_until_visible(*self.FAVORITE_BUTTON)
        fav_button.click()

