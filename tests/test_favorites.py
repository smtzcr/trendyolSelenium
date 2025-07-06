import unittest
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.favorites_page import FavoritesPage
from pages.login_page import LoginPage
from utils import config


class FavoritesTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.favorites_page = FavoritesPage(self.driver)
        self.login_page = LoginPage(self.driver)

        # Login first (required for favorites)
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()
        self.login_page.open_login_form()
        self.login_page.enter_email(config.EMAIL)
        self.login_page.enter_password(config.PASSWORD)
        self.login_page.submit_login()

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_add_product_to_favorites(self):
        """Test adding a product to favorites"""
        self.search_page.search_for("kulaklık")
        self.product_page.click_first_product()
        self.product_page.add_to_favorites()

        self.favorites_page.go_to_favorites()
        self.assertTrue(
            self.favorites_page.is_favorite_listed(),
            "Product not found in favorites"
        )

    def test_favorites_page_access(self):
        """Test accessing favorites page"""
        self.favorites_page.go_to_favorites()

        # Check if we're on favorites page
        current_url = self.driver.current_url
        self.assertIn("favoriler", current_url.lower(), "Not on favorites page")

    def test_add_multiple_favorites(self):
        """Test adding multiple products to favorites"""
        products = ["tablet", "şarj aleti"]

        for product in products:
            self.home_page.go_to("https://www.trendyol.com")
            self.search_page.search_for(product)
            self.product_page.click_first_product()
            self.product_page.add_to_favorites()

        self.favorites_page.go_to_favorites()
        self.assertTrue(
            self.favorites_page.is_favorite_listed(),
            "Multiple favorites not working"
        )

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()