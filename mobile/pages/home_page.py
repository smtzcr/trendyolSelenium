from appium.webdriver.common.appiumby import AppiumBy
from mobile.base.base_page import BasePage

class HomePage(BasePage):
    PUSH_ALLOW_BTN = (AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button")

    def is_push_permission_visible(self):
        return self.is_visible(*self.PUSH_ALLOW_BTN)
