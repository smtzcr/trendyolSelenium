from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class SearchPage(BasePage):
    SEARCH_INPUT = (By.CLASS_NAME, "vQI670rJ")
    SEARCH_BUTTON = (By.XPATH, "//i[@data-testid='search-icon']")
    PRODUCT_CONTAINER = (By.CLASS_NAME, "p-card-wrppr")

    def search_for(self, keyword):
        self.type(*self.SEARCH_INPUT, text=keyword)
        self.click(*self.SEARCH_BUTTON)
        time.sleep(3)

    def is_search_result_loaded(self):
        try:
            container = self.wait_until_visible(*self.PRODUCT_CONTAINER)
            return container.is_displayed()
        except:
            return False
