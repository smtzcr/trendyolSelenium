import unittest
import time
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.search_page import SearchPage


class SearchAdvancedTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_search_multiple_categories(self):
        """Test search with multiple different keywords"""
        keywords = ["telefon", "ayakkabı", "kitap", "gömlek"]

        for keyword in keywords:
            self.search_page.search_for(keyword)
            self.assertTrue(
                self.search_page.is_search_result_loaded(),
                f"Search results not loaded for '{keyword}'"
            )
            time.sleep(1)

    def test_search_with_special_characters(self):
        """Test search functionality with special characters"""
        special_searches = ["t-shirt", "50% indirim", "çanta", "şapka"]

        for search_term in special_searches:
            self.search_page.search_for(search_term)
            # Should not crash, results may or may not be found
            time.sleep(1)

    def test_search_with_numbers(self):
        """Test search with numeric queries"""
        numeric_searches = ["iphone 14", "samsung s23", "ps5"]

        for search_term in numeric_searches:
            self.search_page.search_for(search_term)
            self.assertTrue(
                self.search_page.is_search_result_loaded(),
                f"Search results not loaded for '{search_term}'"
            )
            time.sleep(1)

    def test_search_long_query(self):
        """Test search with very long query"""
        long_query = "çok uzun bir arama sorgusu test ediyoruz burada"
        self.search_page.search_for(long_query)
        # Should handle gracefully

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()