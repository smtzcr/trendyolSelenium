from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def go_to(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def click(self, by, value):
        self.find(by, value).click()

    def type(self, by, value, text):
        self.find(by, value).send_keys(text)

    def wait_until_visible(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))

    def is_element_displayed(self, by, value):
        try:
            return self.find(by, value).is_displayed()
        except:
            return False

    def close_popup_if_present(self):
        try:
            popup_close = self.driver.find_element(By.CLASS_NAME, "modal-close")
            if popup_close.is_displayed():
                popup_close.click()
        except (NoSuchElementException, ElementClickInterceptedException):
            pass

    def scroll_to_element_in_filter_panel(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            return element
        except Exception as e:
            print(f"[SCROLL ERROR]: {e}")
            return None

    def switch_to_new_tab(self):
        windows = self.driver.window_handles
        if len(windows) > 1:
            self.driver.switch_to.window(windows[-1])

