import unittest
from utils.driver_factory import create_driver
from pages.home_page import HomePage

class HomePageTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.home_page.go_to("https://www.trendyol.com")

    def test_homepage_loads_successfully(self):
        self.assertTrue(self.home_page.is_logo_visible(), "Logo doesn't exist!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
