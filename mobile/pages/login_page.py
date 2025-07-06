from appium.webdriver.common.appiumby import AppiumBy

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    MY_ACCOUNT_BUTTON = (AppiumBy.ID, "trendyol.com:id/tab_account")
    LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.GridView[@resource-id='trendyol.com:id/recyclerViewAccount']/androidx.compose.ui.platform.ComposeView[1]/android.view.View/android.view.View/android.view.View/android.widget.Button")
    EMAIL_INPUT = (AppiumBy.ID, "trendyol.com:id/editTextEmail")
    NEXT_STEP_BUTTON = (AppiumBy.ID, "trendyol.com:id/buttonContinue")
    PASSWORD_INPUT = (AppiumBy.ID, "trendyol.com:id/editTextPassword")
    SUBMIT_BUTTON = (AppiumBy.ID, "trendyol.com:id/buttonLogin")
    USER_LABEL = (AppiumBy.ID, "trendyol.com:id/textViewEmail")

    def tap_login_button(self):
        self.driver.find_element(*self.MY_ACCOUNT_BUTTON).click()
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def enter_credentials(self, email, password):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.NEXT_STEP_BUTTON).click()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def is_logged_in(self):
        return self.driver.find_element(*self.USER_LABEL).is_displayed()