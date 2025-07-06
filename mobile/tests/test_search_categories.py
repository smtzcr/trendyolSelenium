import unittest
import time
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage
from mobile.pages.search_page import SearchPage


class MobileSearchCategoriesTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'screenshots/mobile_{test_name}_{timestamp}.png'
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def test_search_multiple_categories(self):
        """Test search with different product categories"""
        categories = ["laptop", "ayakkabı", "gömlek", "çanta", "kitap"]

        for category in categories:
            self.home_page.go_to_home_page()
            self.home_page.tap_search_bar()
            self.search_page.search(category)
            self.assertTrue(
                self.search_page.has_results(),
                f"Search results not loaded for '{category}'"
            )
            time.sleep(1)

    def test_search_electronics(self):
        """Test search for electronics category"""
        electronics = ["telefon", "laptop", "kulaklık", "tablet"]

        for item in electronics:
            self.home_page.go_to_home_page()
            self.home_page.tap_search_bar()
            self.search_page.search(item)
            self.assertTrue(
                self.search_page.has_results(),
                f"Search results not loaded for '{item}'"
            )

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()