import unittest
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage
from mobile.pages.search_page import SearchPage
from mobile.pages.product_detail_page import ProductDetailPage

class ProductDetailTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.detail_page = ProductDetailPage(self.driver)

    def test_navigate_to_product_detail(self):
        self.home_page.tap_search_bar()
        self.search_page.search("sneaker")
        self.search_page.select_first_product()

        self.assertTrue(
            self.detail_page.is_product_title_visible(),
            "Product detail page is not opened!"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

