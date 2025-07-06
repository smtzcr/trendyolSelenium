import time
from appium.webdriver.common.appiumby import AppiumBy

class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    SEARCH_INPUT = (AppiumBy.ID, "trendyol.com:id/editTextSearchView")
    FIRST_RESULT = (AppiumBy.XPATH, "(//android.view.View[@resource-id='VerticalProductCard'])[1]")
    FIRST_SUGGESTION = (AppiumBy.XPATH, "(//android.view.ViewGroup[@resource-id='trendyol.com:id/constraintLayoutItemSearchAutoComplete'])[1]")

    def search(self, keyword):
        input_box = self.driver.find_element(*self.SEARCH_INPUT)
        input_box.send_keys(keyword)
        time.sleep(2)
        self.driver.find_element(*self.FIRST_SUGGESTION).click()

    def has_results(self):
        return len(self.driver.find_elements(*self.FIRST_RESULT)) > 0

    def select_first_product(self):
        self.driver.find_element(*self.FIRST_RESULT).click()