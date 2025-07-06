import unittest
from utils.driver_factory import create_driver
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils import config


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.home_page.go_to("https://www.trendyol.com")
        self.home_page.close_popup_if_present()

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        return self.home_page.take_screenshot(test_name)

    def test_login_with_valid_credentials(self):
        """Test login with valid credentials"""
        self.login_page.open_login_form()
        self.login_page.enter_email(config.EMAIL)
        self.login_page.enter_password(config.PASSWORD)
        self.login_page.submit_login()

        self.assertTrue(
            self.login_page.is_user_logged_in(),
            "Login failed with valid credentials"
        )

    def test_login_form_opens(self):
        """Test if login form opens correctly"""
        self.login_page.open_login_form()

        # Check if email input is visible
        try:
            email_input = self.driver.find_element(*self.login_page.EMAIL_INPUT)
            self.assertTrue(email_input.is_displayed(), "Email input not visible")
        except:
            self.fail("Login form did not open properly")

    def test_login_form_elements(self):
        """Test if all login form elements are present"""
        self.login_page.open_login_form()

        # Check email input
        email_input = self.driver.find_element(*self.login_page.EMAIL_INPUT)
        self.assertTrue(email_input.is_displayed(), "Email input not visible")

        # Enter email to proceed to password step
        self.login_page.enter_email(config.EMAIL)

        # Check password input
        password_input = self.driver.find_element(*self.login_page.PASSWORD_INPUT)
        self.assertTrue(password_input.is_displayed(), "Password input not visible")

        # Check submit button
        submit_button = self.driver.find_element(*self.login_page.SUBMIT_BUTTON)
        self.assertTrue(submit_button.is_displayed(), "Submit button not visible")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()