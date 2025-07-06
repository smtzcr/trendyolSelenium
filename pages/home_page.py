from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    LOGO = (By.CLASS_NAME, "logo")

    def is_logo_visible(self):
        return self.is_element_displayed(*self.LOGO)