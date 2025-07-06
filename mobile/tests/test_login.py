import unittest
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.login_page import LoginPage

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.login_page = LoginPage(self.driver)

    def test_login_successful(self):
        self.login_page.tap_login_button()
        self.login_page.enter_credentials("smettommer@gmail.com", "smoss1905A")
        self.assertTrue(
            self.login_page.is_logged_in(),
            "Login failed!"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
