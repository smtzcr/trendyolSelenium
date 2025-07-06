import unittest
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage

class AppLaunchTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'screenshots/mobile_{test_name}_{timestamp}.png'
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def test_app_launch_successful(self):
        """Test if app launches successfully and home screen loads"""
        self.assertTrue(
            self.home_page.is_search_icon_visible(),
            "App didn't launch properly or search icon not visible"
        )

    def test_home_screen_elements(self):
        """Test if main home screen elements are visible"""
        self.assertTrue(
            self.home_page.is_search_icon_visible(),
            "Search icon not visible on home screen"
        )

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()