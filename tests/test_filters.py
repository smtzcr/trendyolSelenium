import unittest
import time
from utils.driver_factory import create_driver
from pages.filter_page import FilterPage


class FilterTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.filter_page = FilterPage(self.driver)
        self.filter_page.go_to_category_page()
        time.sleep(3)
        self.filter_page.close_popup_if_present()

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.filter_page.take_screenshot(test_name)

    def test_price_filter(self):
        """Test price filtering functionality"""
        self.filter_page.apply_price_filter(min_price=100, max_price=600)
        time.sleep(3)

        self.assertTrue(
            self.filter_page.all_prices_within_range(100, 600),
            "Price filter not working correctly"
        )

    def test_gender_filter(self):
        """Test gender filter functionality"""
        self.filter_page.apply_gender_filter()
        time.sleep(2)

        # Check if filter was applied (products should be visible)
        from selenium.webdriver.common.by import By
        products = self.driver.find_elements(By.CLASS_NAME, "p-card-wrppr")
        self.assertGreater(len(products), 0, "No products found after gender filter")

    def test_price_and_gender_filter_combined(self):
        """Test combining price and gender filters"""
        self.filter_page.apply_gender_filter()
        time.sleep(3)
        self.filter_page.apply_price_filter(min_price=100, max_price=600)
        time.sleep(2)

        self.assertTrue(
            self.filter_page.all_prices_within_range(100, 600),
            "Combined filters not working correctly"
        )

    def test_filter_clear_functionality(self):
        """Test clearing filters"""
        # Apply filters first
        self.filter_page.apply_price_filter(min_price=200, max_price=400)
        time.sleep(2)

        # Navigate back to category page (this clears filters)
        self.filter_page.go_to_category_page()
        time.sleep(2)

        # Check if more products are visible (filter cleared)
        from selenium.webdriver.common.by import By
        products = self.driver.find_elements(By.CLASS_NAME, "p-card-wrppr")
        self.assertGreater(len(products), 0, "Products not visible after filter clear")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()