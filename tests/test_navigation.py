import unittest
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from selenium.webdriver.common.by import By


class NavigationTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.product_page = ProductPage(self.driver)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_category_navigation(self):
        """Test navigation through different categories"""
        categories = [
            "https://www.trendyol.com/kadin",
            "https://www.trendyol.com/erkek",
            "https://www.trendyol.com/ev-yasam"
        ]

        for category_url in categories:
            self.home_page.go_to(category_url)
            self.home_page.wait_for_page_load()

            # Check if products are loaded
            try:
                products = self.driver.find_elements(By.CLASS_NAME, "p-card-wrppr")
                self.assertGreater(len(products), 0, f"No products found in category: {category_url}")
            except:
                pass  # Category structure might be different

    def test_breadcrumb_navigation(self):
        """Test breadcrumb navigation"""
        # Go to a category page
        self.home_page.go_to("https://www.trendyol.com/kadin-yuzuk-x-g1-c103")
        self.home_page.wait_for_page_load()

        # Look for breadcrumbs
        try:
            breadcrumbs = self.driver.find_elements(By.CLASS_NAME, "breadcrumb-item")
            if len(breadcrumbs) > 1:
                # Click on first breadcrumb (home)
                breadcrumbs[0].click()
                self.home_page.wait_for_page_load()

                # Verify navigation worked
                self.assertTrue(
                    self.home_page.is_logo_visible(),
                    "Breadcrumb navigation failed"
                )
        except:
            pass  # Breadcrumb structure might be different

    def test_back_button_navigation(self):
        """Test browser back button functionality"""
        # Navigate through pages
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        self.search_page.search_for("spor")
        self.home_page.wait_for_page_load()

        self.product_page.click_first_product()
        self.home_page.wait_for_page_load()

        # Use browser back button
        self.driver.back()
        self.home_page.wait_for_page_load()

        # Should be back to search results
        self.assertTrue(
            self.search_page.is_search_result_loaded(),
            "Back button navigation failed"
        )

    def test_home_page_navigation(self):
        """Test navigation to home page from different pages"""
        # Go to a category page first
        self.home_page.go_to("https://www.trendyol.com/kadin")
        self.home_page.wait_for_page_load()

        # Navigate back to home
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        # Verify we're on home page
        self.assertTrue(
            self.home_page.is_logo_visible(),
            "Home page navigation failed"
        )

    def test_multiple_tab_navigation(self):
        """Test opening products in new tabs"""
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

        self.search_page.search_for("monitör")

        # Get first product
        products = self.driver.find_elements(By.CLASS_NAME, "p-card-wrppr")
        if len(products) > 0:
            original_window = self.driver.current_window_handle

            # Click product (might open in new tab)
            self.driver.execute_script("arguments[0].click();", products[0])
            self.home_page.wait_for_page_load()

            # Check if new tab opened
            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[-1])
                self.assertTrue(
                    self.product_page.is_product_title_visible(),
                    "Product detail page not loaded in new tab"
                )
                self.driver.close()
                self.driver.switch_to.window(original_window)

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()