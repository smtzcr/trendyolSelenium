import unittest
from utils.driver_factory import create_driver
from pages.search_page import SearchPage

class SearchTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.search_page = SearchPage(self.driver)
        self.search_page.go_to("https://www.trendyol.com")
        self.search_page.close_popup_if_present()

    def test_search_functionality(self):
        self.search_page.search_for("ayakkabı")
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Search results not loaded!"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
