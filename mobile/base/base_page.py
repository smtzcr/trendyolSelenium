from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def click(self, by, value):
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def is_visible(self, by, value):
        try:
            return self.wait.until(EC.visibility_of_element_located((by, value))).is_displayed()
        except:
            return False
