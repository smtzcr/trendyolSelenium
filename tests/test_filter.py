import unittest
from utils.driver_factory import create_driver
from pages.filter_page import FilterPage
import time

class FilterTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.page = FilterPage(self.driver)
        self.page.go_to_category_page()
        time.sleep(3)
        self.page.close_popup_if_present()

    def test_price_and_gender_filter(self):
        self.page.apply_gender_filter()
        time.sleep(3)
        self.page.apply_price_filter(min_price=100, max_price=600)
        time.sleep(2)
        self.assertTrue(
            self.page.all_prices_within_range(100, 600),
            "Fiyat filtresine uymayan ürünler listelenmiş."
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
