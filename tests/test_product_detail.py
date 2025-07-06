import unittest
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage


class ProductDetailTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_product_detail_navigation(self):
        """Test navigation to product detail page"""
        self.search_page.search_for("klavye")
        self.assertTrue(self.search_page.is_search_result_loaded())

        self.product_page.click_first_product()
        self.assertTrue(
            self.product_page.is_product_title_visible(),
            "Product title not visible on detail page"
        )

    def test_product_elements_visible(self):
        """Test if all product elements are visible on detail page"""
        self.search_page.search_for("mouse")
        self.product_page.click_first_product()

        self.assertTrue(
            self.product_page.is_product_title_visible(),
            "Product title not visible"
        )
        self.assertTrue(
            self.product_page.is_product_price_visible(),
            "Product price not visible"
        )
        self.assertTrue(
            self.product_page.is_add_to_cart_visible(),
            "Add to cart button not visible"
        )

    def test_multiple_product_navigation(self):
        """Test navigating to multiple different products"""
        search_terms = ["monitör", "kulaklık", "telefon"]

        for term in search_terms:
            self.search_page.search_for(term)
            self.product_page.click_first_product()

            self.assertTrue(
                self.product_page.is_product_title_visible(),
                f"Product detail not loaded for {term}"
            )

            # Go back to home for next search
            self.home_page.go_to("https://www.trendyol.com")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()