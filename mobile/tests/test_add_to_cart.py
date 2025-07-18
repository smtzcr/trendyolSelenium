import unittest
import time
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage
from mobile.pages.search_page import SearchPage
from mobile.pages.product_detail_page import ProductDetailPage
from mobile.pages.cart_page import CartPage


class MobileAddToCartTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.detail_page = ProductDetailPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'screenshots/mobile_{test_name}_{timestamp}.png'
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def test_add_product_to_cart(self):
        """Test adding a product to cart on mobile"""
        self.home_page.tap_search_bar()
        self.search_page.search("mouse")
        self.search_page.select_first_product()
        self.detail_page.add_to_cart()

        self.assertTrue(
            self.cart_page.is_product_in_cart(),
            "Product wasn't added to cart successfully"
        )

    def test_cart_functionality(self):
        """Test comprehensive cart operations on mobile"""
        # Add product to cart
        self.home_page.tap_search_bar()
        self.search_page.search("telefon kılıfı")
        self.search_page.select_first_product()
        self.detail_page.add_to_cart()

        # Go to cart
        self.cart_page.go_to_cart()

        self.assertTrue(
            self.cart_page.is_product_in_cart(),
            "Cart operations failed on mobile"
        )

    def test_add_multiple_products(self):
        """Test adding multiple products to cart"""
        products = ["klavye", "mouse"]

        for product in products:
            self.home_page.go_to_home_page()
            self.home_page.tap_search_bar()
            self.search_page.search(product)
            self.search_page.select_first_product()
            self.detail_page.add_to_cart()
            time.sleep(1)

        self.assertTrue(
            self.cart_page.is_product_in_cart(),
            "Multiple products not added to cart"
        )

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()