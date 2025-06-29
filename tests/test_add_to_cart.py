import time
import unittest
from utils.driver_factory import create_driver
from pages.product_page import ProductPage
from pages.cart_page import CartPage

class AddToCartTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.product_page.go_to("https://www.trendyol.com/kadin-yuzuk-x-g1-c103")
        self.product_page.close_popup_if_present()

    def test_add_to_cart(self):
        self.product_page.click_first_product()
        self.assertTrue(self.product_page.is_add_to_cart_visible(), "Sepete Ekle butonu görünmüyor!")
        self.product_page.add_to_cart()
        time.sleep(2)
        self.cart_page.go_to_cart()
        self.assertTrue(self.cart_page.is_product_in_cart(), "Ürün sepette görünmüyor!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
