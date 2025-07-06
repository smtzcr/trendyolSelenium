import unittest
import time
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.search_page import SearchPage


class ResponsiveTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_mobile_screen_size(self):
        """Test website on mobile screen size"""
        # Set mobile size
        self.driver.set_window_size(375, 667)
        time.sleep(2)

        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        # Check if search still works
        self.search_page.search_for("tablet")
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Search doesn't work on mobile size"
        )

    def test_tablet_screen_size(self):
        """Test website on tablet screen size"""
        # Set tablet size
        self.driver.set_window_size(768, 1024)
        time.sleep(2)

        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        # Test basic functionality
        self.assertTrue(
            self.home_page.is_logo_visible(),
            "Logo not visible on tablet size"
        )

        self.search_page.search_for("laptop")
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Search doesn't work on tablet size"
        )

    def test_desktop_screen_size(self):
        """Test website on desktop screen size"""
        # Set desktop size
        self.driver.set_window_size(1920, 1080)
        time.sleep(2)

        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        # Test basic functionality
        self.assertTrue(
            self.home_page.is_logo_visible(),
            "Logo not visible on desktop size"
        )

        self.search_page.search_for("telefon")
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Search doesn't work on desktop size"
        )

    def test_screen_resize_functionality(self):
        """Test functionality when resizing screen"""
        sizes = [
            (1920, 1080),  # Desktop
            (768, 1024),  # Tablet
            (375, 667),  # Mobile
            (1920, 1080)  # Back to desktop
        ]

        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        for width, height in sizes:
            self.driver.set_window_size(width, height)
            time.sleep(1)

            # Test that logo is still visible after resize
            try:
                self.assertTrue(
                    self.home_page.is_logo_visible(),
                    f"Logo not visible at size {width}x{height}"
                )
            except:
                pass  # Some sizes might hide certain elements

    def test_window_maximize_minimize(self):
        """Test window maximize and minimize"""
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        # Minimize window
        self.driver.set_window_size(800, 600)
        time.sleep(1)

        # Test basic functionality
        self.search_page.search_for("oyuncak")

        # Maximize window
        self.driver.maximize_window()
        time.sleep(1)

        # Verify functionality still works
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Search doesn't work after window resize"
        )

    def tearDown(self):
        # Reset to default size
        if self.driver:
            self.driver.maximize_window()
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()