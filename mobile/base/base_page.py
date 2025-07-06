from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from datetime import datetime


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'screenshots/mobile_{test_name}_{timestamp}.png'
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def click(self, by, value):
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def is_visible(self, by, value):
        try:
            return self.wait.until(EC.visibility_of_element_located((by, value))).is_displayed()
        except:
            return False