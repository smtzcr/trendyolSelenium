from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


def create_driver():
    print("🚀 ChromeDriver başlatılıyor...")

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Proje klasöründeki chromedriver.exe'yi kullan
    current_dir = os.getcwd()
    driver_path = os.path.join(current_dir, "chromedriver/chromedriver.exe")

    print(f"📁 Proje klasörü: {current_dir}")
    print(f"🔍 ChromeDriver aranıyor: {driver_path}")
    print(f"📂 Dosya var mı: {os.path.exists(driver_path)}")

    if os.path.exists(driver_path):
        try:
            print(f"✅ ChromeDriver bulundu: {driver_path}")
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            print("🎉 Chrome browser açıldı!")
            return driver
        except Exception as e:
            print(f"❌ ChromeDriver hatası: {e}")
    else:
        print(f"❌ ChromeDriver bulunamadı: {driver_path}")

    # System PATH'den dene
    try:
        print("🔄 System PATH'den deneniyor...")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ System PATH'den başarılı!")
        return driver
    except Exception as e:
        print(f"❌ System PATH hatası: {e}")

    raise Exception("❌ ChromeDriver hiçbir şekilde bulunamadı!")


def get_driver():
    return create_driver()