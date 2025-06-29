from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FavoritesPage(BasePage):
    FAVORITES_URL = "https://www.trendyol.com/Hesabim/Favoriler"

    FAVORITE_ITEMS = (By.CLASS_NAME, "favorite-wrapper")  # Favorideki ürün kartları

    def go_to_favorites(self):
        self.go_to(self.FAVORITES_URL)

    def is_favorite_listed(self):
        try:
            fav = self.wait_until_visible(*self.FAVORITE_ITEMS)
            return fav.is_displayed()
        except:
            return False
