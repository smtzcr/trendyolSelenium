import os

capabilities = {
    "platformName": "Android",
    "appium:deviceName": "emulator-5554",
    "appium:automationName": "UiAutomator2",
    "appium:app": os.path.join(os.getcwd(), "mobile", "apps", "trendyol.apk"),
    "appium:autoGrantPermissions": True,
    "appium:noReset": True,
    "appium:newCommandTimeout": 300
}