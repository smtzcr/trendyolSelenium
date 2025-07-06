import unittest
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage
from mobile.pages.search_page import SearchPage
from mobile.pages.product_detail_page import ProductDetailPage
from mobile.pages.cart_page import CartPage

class AddToCartTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.detail_page = ProductDetailPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def test_add_product_to_cart(self):
        self.home_page.tap_search_bar()
        self.search_page.search("kalem")
        self.search_page.select_first_product()
        self.detail_page.add_to_cart()

        self.assertTrue(
            self.cart_page.is_product_in_cart(),
            "Ürün sepette görünmüyor!"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
