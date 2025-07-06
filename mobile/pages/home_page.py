from appium.webdriver.common.appiumby import AppiumBy

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    SEARCH_ICON = (AppiumBy.ID, "trendyol.com:id/imageViewSearch")
    SEARCH_BAR = (AppiumBy.ID, "trendyol.com:id/editTextSearchView")
    HOME_PAGE_TAB_BUTTON = (AppiumBy.ID, "trendyol.com:id/tab_home")

    def is_search_icon_visible(self):
        return self.driver.find_element(*self.SEARCH_ICON).is_displayed()

    def tap_search_bar(self):
        self.driver.find_element(*self.SEARCH_BAR).click()

    def go_to_home_page(self):
        self.driver.find_element(*self.HOME_PAGE_TAB_BUTTON).click()