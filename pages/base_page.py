import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import json
import logging


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        if not os.path.exists('logs'):
            os.makedirs('logs')

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def take_screenshot(self, test_name):
        """Take screenshot for error reporting"""
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'screenshots/{test_name}_{timestamp}.png'
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def log_error(self, test_name, error_message, exception=None):
        """Log error with screenshot and details"""
        screenshot_path = self.take_screenshot(test_name)

        error_data = {
            'timestamp': datetime.now().isoformat(),
            'test_name': test_name,
            'error_message': error_message,
            'screenshot_path': screenshot_path,
            'url': self.driver.current_url,
            'page_title': self.driver.title,
            'exception': str(exception) if exception else None
        }

        # Save error to JSON file for Grafana consumption
        if not os.path.exists('reports'):
            os.makedirs('reports')

        error_file = f'reports/errors_{datetime.now().strftime("%Y%m%d")}.json'

        if os.path.exists(error_file):
            with open(error_file, 'r') as f:
                errors = json.load(f)
        else:
            errors = []

        errors.append(error_data)

        with open(error_file, 'w') as f:
            json.dump(errors, f, indent=2)

        self.logger.error(f"Test failed: {test_name} - {error_message}")
        return error_data

    def go_to(self, url):
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.log_error("navigation", f"Failed to navigate to {url}", e)
            raise

    def find(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException as e:
            self.log_error("element_find", f"Element not found: {by}={value}", e)
            raise

    def click(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            self.logger.info(f"Clicked element: {by}={value}")
        except Exception as e:
            self.log_error("element_click", f"Failed to click element: {by}={value}", e)
            raise

    def type(self, by, value, text, timeout=10):
        try:
            element = self.find(by, value, timeout)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Typed '{text}' into element: {by}={value}")
        except Exception as e:
            self.log_error("element_type", f"Failed to type into element: {by}={value}", e)
            raise

    def wait_until_visible(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException as e:
            self.log_error("element_visibility", f"Element not visible: {by}={value}", e)
            raise

    def is_element_displayed(self, by, value, timeout=5):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element.is_displayed()
        except:
            return False

    def close_popup_if_present(self):
        """Close any popup that might appear"""
        popup_selectors = [
            (By.CLASS_NAME, "modal-close"),
            (By.CLASS_NAME, "popup-close"),
            (By.XPATH, "//button[contains(@class, 'close')]"),
            (By.XPATH, "//div[contains(@class, 'close')]"),
            (By.ID, "cookieUsagePopupAccept")
        ]

        for selector in popup_selectors:
            try:
                popup = self.driver.find_element(*selector)
                if popup.is_displayed():
                    popup.click()
                    time.sleep(1)
                    self.logger.info(f"Closed popup: {selector}")
                    break
            except (NoSuchElementException, ElementClickInterceptedException):
                continue

    def scroll_to_element(self, by, value):
        try:
            element = self.find(by, value)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            return element
        except Exception as e:
            self.log_error("scroll_to_element", f"Failed to scroll to element: {by}={value}", e)
            return None

    def switch_to_new_tab(self):
        try:
            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[-1])
                self.logger.info("Switched to new tab")
        except Exception as e:
            self.log_error("tab_switch", "Failed to switch to new tab", e)
            raise

    def get_text(self, by, value, timeout=10):
        try:
            element = self.find(by, value, timeout)
            return element.text
        except Exception as e:
            self.log_error("get_text", f"Failed to get text from element: {by}={value}", e)
            raise

    def wait_for_page_load(self, timeout=30):
        """Wait for page to fully load"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("Page loaded successfully")
        except TimeoutException as e:
            self.log_error("page_load", "Page load timeout", e)
            raise