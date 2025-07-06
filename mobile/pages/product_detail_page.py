from appium.webdriver.common.appiumby import AppiumBy

class ProductDetailPage:
    def __init__(self, driver):
        self.driver = driver

    PRODUCT_TITLE = (AppiumBy.ID, "trendyol.com:id/productNameView")
    ADD_TO_CART_BUTTON = (AppiumBy.ID, "trendyol.com:id/primaryButton")
    FAVORITE_ICON = (AppiumBy.ID, "trendyol.com:id/favorite_product_detail")
    RETURN_BUTTON = (AppiumBy.ID, "trendyol.com:id/imageViewBack")

    def is_product_title_visible(self):
        return self.driver.find_element(*self.PRODUCT_TITLE).is_displayed()

    def add_to_cart(self):
        self.driver.find_element(*self.ADD_TO_CART_BUTTON).click()

    def add_to_favorites(self):
        self.driver.find_element(*self.FAVORITE_ICON).click()

    def exit_product(self):
        self.driver.find_element(*self.RETURN_BUTTON).click()