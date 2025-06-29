import unittest
from appium import webdriver
from mobile.config import capabilities
from mobile.pages.home_page import HomePage

class PushNotificationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)

    def test_push_permission_popup(self):
        self.assertTrue(
            self.home_page.is_push_permission_visible(),
            "Push bildirimi popup'ı görünmüyor!"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
