from appium.webdriver.common.appiumby import AppiumBy

class CartPage:
    def __init__(self, driver):
        self.driver = driver

    CART_ICON = (AppiumBy.ID, "trendyol.com:id/productDetailBasket")
    PRODUCT_IN_CART = (AppiumBy.XPATH, "(//android.widget.ImageView[@resource-id='trendyol.com:id/imageViewItemBasketProducts'])")

    def go_to_cart(self):
        self.driver.find_element(*self.CART_ICON).click()

    def is_product_in_cart(self):
        return len(self.driver.find_elements(*self.PRODUCT_IN_CART)) > 0
