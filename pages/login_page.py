from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    LOGIN_BUTTON_HEADER = (By.CLASS_NAME, "user-login-container")
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password-input")
    SUBMIT_BUTTON = (By.CLASS_NAME, "q-primary")
    USERNAME_LABEL = (By.XPATH, '//*[@id="account-navigation-container"]/div/div[1]/div[1]/p')

    def open_login_form(self):
        self.click(*self.LOGIN_BUTTON_HEADER)

    def enter_email(self, email):
        self.type(*self.EMAIL_INPUT, text=email)

    def enter_password(self, password):
        self.type(*self.PASSWORD_INPUT, text=password)

    def submit_login(self):
        self.click(*self.SUBMIT_BUTTON)
        time.sleep(3)

    def is_user_logged_in(self):
        element = self.wait_until_visible(*self.USERNAME_LABEL)
        return element.text.strip() == "Hesabım"