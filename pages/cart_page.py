from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_BUTTON = (By.CLASS_NAME, "account-basket")  # Üstteki sepet ikonu
    CART_ITEM = (By.CLASS_NAME, "pb-basket-item-wrapper-v2")  # Sepetteki ürün kutusu

    def go_to_cart(self):
        self.click(*self.CART_BUTTON)

    def is_product_in_cart(self):
        try:
            item = self.wait_until_visible(*self.CART_ITEM)
            return item.is_displayed()
        except:
            return False