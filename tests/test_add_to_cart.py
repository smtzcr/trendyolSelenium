import unittest
import time
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class AddToCartTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_add_product_to_cart(self):
        """Test adding a product to cart"""
        self.search_page.search_for("mouse")
        self.product_page.click_first_product()

        self.assertTrue(
            self.product_page.is_add_to_cart_visible(),
            "Add to cart button not visible"
        )

        self.product_page.add_to_cart()
        time.sleep(2)

        self.cart_page.go_to_cart()
        self.assertTrue(
            self.cart_page.is_product_in_cart(),
            "Product not found in cart"
        )

    def test_add_multiple_products_to_cart(self):
        """Test adding multiple products to cart"""
        products = ["klavye", "mouse"]

        for product in products:
            self.home_page.go_to("https://www.trendyol.com")
            self.search_page.search_for(product)
            self.product_page.click_first_product()
            self.product_page.add_to_cart()
            time.sleep(1)

        self.cart_page.go_to_cart()
        self.assertTrue(
            self.cart_page.is_product_in_cart(),
            "Products not found in cart"
        )

    def test_cart_button_functionality(self):
        """Test cart button navigation"""
        # First add a product
        self.search_page.search_for("kulaklık")
        self.product_page.click_first_product()
        self.product_page.add_to_cart()
        time.sleep(2)

        # Test cart navigation
        self.cart_page.go_to_cart()

        # Verify we're on cart page
        current_url = self.driver.current_url
        self.assertIn("sepet", current_url.lower(), "Not navigated to cart page")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()