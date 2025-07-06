import unittest
import time
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage
from mobile.pages.search_page import SearchPage
from mobile.pages.product_detail_page import ProductDetailPage


class MobileProductNavigationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.detail_page = ProductDetailPage(self.driver)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'screenshots/mobile_{test_name}_{timestamp}.png'
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def test_product_detail_navigation(self):
        """Test navigation to product detail page"""
        self.home_page.tap_search_bar()
        self.search_page.search("kulaklık")
        self.search_page.select_first_product()

        self.assertTrue(
            self.detail_page.is_product_title_visible(),
            "Product detail page didn't load properly"
        )

    def test_multiple_product_views(self):
        """Test viewing multiple products in sequence"""
        products_to_search = ["klavye", "monitör", "fare"]

        for product in products_to_search:
            self.home_page.go_to_home_page()
            self.home_page.tap_search_bar()
            self.search_page.search(product)
            self.search_page.select_first_product()

            self.assertTrue(
                self.detail_page.is_product_title_visible(),
                f"Product detail not loaded for {product}"
            )

            self.detail_page.exit_product()
            time.sleep(1)

    def test_product_back_navigation(self):
        """Test navigating back from product detail"""
        self.home_page.tap_search_bar()
        self.search_page.search("tablet")
        self.search_page.select_first_product()

        # Verify we're on product detail
        self.assertTrue(
            self.detail_page.is_product_title_visible(),
            "Not on product detail page"
        )

        # Navigate back
        self.detail_page.exit_product()

        # Verify we're back to search results
        self.assertTrue(
            self.search_page.has_results(),
            "Not back to search results"
        )

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()