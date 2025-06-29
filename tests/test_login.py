import unittest
from utils.driver_factory import create_driver
from pages.login_page import LoginPage
from utils import config

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = create_driver()
        self.login_page = LoginPage(self.driver)
        self.login_page.go_to("https://www.trendyol.com")
        self.login_page.close_popup_if_present()

    def test_login_with_valid_credentials(self):
        self.login_page.open_login_form()
        self.login_page.enter_email(config.EMAIL)
        self.login_page.enter_password(config.PASSWORD)
        self.login_page.submit_login()
        self.assertTrue(self.login_page.is_user_logged_in(), "Login failed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
