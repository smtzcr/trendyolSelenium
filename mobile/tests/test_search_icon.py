import unittest
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage

class SearchIconTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)

    def test_search_icon_visible(self):
        self.assertTrue(
            self.home_page.is_search_icon_visible(),
            "Search icon is not visible!"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
