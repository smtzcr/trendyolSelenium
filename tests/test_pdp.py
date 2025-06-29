import unittest
from utils.driver_factory import create_driver
from pages.product_page import ProductPage

class ProductDetailTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.page = ProductPage(self.driver)
        self.page.go_to("https://www.trendyol.com/kadin-yuzuk-x-g1-c103")
        self.page.close_popup_if_present()

    def test_product_detail_page_elements(self):
        self.page.click_first_product()
        self.assertTrue(self.page.is_product_title_visible(), "Ürün başlığı görünmüyor!")
        self.assertTrue(self.page.is_product_price_visible(), "Ürün fiyatı görünmüyor!")
        self.assertTrue(self.page.is_add_to_cart_visible(), "Sepete Ekle butonu görünmüyor!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
