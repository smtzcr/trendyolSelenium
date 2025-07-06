# simple_test.py dosyası oluşturun
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

try:
    driver_path = os.path.join(os.getcwd(), "chromedriver/chromedriver.exe")
    print(f"Driver path: {driver_path}")
    print(f"File exists: {os.path.exists(driver_path)}")

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.google.com")
    print(f"Success! Page title: {driver.title}")

    driver.quit()
    print("Test completed successfully!")

except Exception as e:
    print(f"Error: {e}")