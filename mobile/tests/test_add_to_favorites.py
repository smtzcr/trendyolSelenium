import unittest
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage
from mobile.pages.search_page import SearchPage
from mobile.pages.product_detail_page import ProductDetailPage
from mobile.pages.favorites_page import FavoritesPage
from mobile.pages.login_page import LoginPage

class AddToFavoritesTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.login_page = LoginPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.detail_page = ProductDetailPage(self.driver)
        self.favorites_page = FavoritesPage(self.driver)
        self.login_page.tap_login_button()
        self.login_page.enter_credentials("smettommer@gmail.com", "smoss1905A")

    def test_add_to_favorites(self):
        self.home_page.go_to_home_page()
        self.home_page.tap_search_bar()
        self.search_page.search("samsung")
        self.search_page.select_first_product()
        self.detail_page.add_to_favorites()
        self.detail_page.exit_product()
        self.favorites_page.go_to_favorites()

        self.assertTrue(
            self.favorites_page.is_product_in_favorites(),
            "Ürün favorilere eklenemedi!"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
