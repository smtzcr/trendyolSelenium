import unittest
from utils.driver_factory import create_driver
from pages.product_page import ProductPage
from pages.favorites_page import FavoritesPage
from pages.login_page import LoginPage
from utils import config

class FavoritesTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.login_page = LoginPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.favorites_page = FavoritesPage(self.driver)

        self.login_page.go_to("https://www.trendyol.com")
        self.login_page.close_popup_if_present()
        self.login_page.open_login_form()
        self.login_page.enter_email(config.EMAIL)
        self.login_page.enter_password(config.PASSWORD)
        self.login_page.submit_login()

    def test_add_product_to_favorites(self):
        self.product_page.go_to("https://www.trendyol.com/kadin-yuzuk-x-g1-c103")
        self.product_page.click_first_product()
        self.product_page.add_to_favorites()

        self.favorites_page.go_to_favorites()
        self.assertTrue(self.favorites_page.is_favorite_listed(), "Favorilerde ürün bulunamadı.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
