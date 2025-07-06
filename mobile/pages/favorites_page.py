from appium.webdriver.common.appiumby import AppiumBy

class FavoritesPage:
    def __init__(self, driver):
        self.driver = driver

    FAVORITES_TAB = (AppiumBy.ID, "trendyol.com:id/tab_favorites")
    FAVORITE_PRODUCT = (AppiumBy.XPATH, "(//android.widget.ImageView[@resource-id='trendyol.com:id/imageViewFavoriteItem'])")

    def go_to_favorites(self):
        self.driver.find_element(*self.FAVORITES_TAB).click()

    def is_product_in_favorites(self):
        return len(self.driver.find_elements(*self.FAVORITE_PRODUCT)) > 0