import unittest
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.search_page import SearchPage

class SearchBasicTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_search_functionality_basic(self):
        """Test basic search functionality"""
        self.search_page.search_for("laptop")
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Search results not loaded for 'laptop'"
        )

    def test_search_with_turkish_characters(self):
        """Test search with Turkish characters"""
        self.search_page.search_for("çanta")
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Search results not loaded for 'çanta'"
        )

    def test_search_empty_query(self):
        """Test search with empty query"""
        self.search_page.search_for("")
        # Should handle gracefully without crashing

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()