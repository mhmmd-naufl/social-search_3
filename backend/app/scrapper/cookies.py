from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from .config import PATH, CHROMEDRIVER_PATH

def get_new_cookies():
    """Mengambil cookies dari TikTok menggunakan Selenium."""
    options = Options()
    options.binary_location = PATH
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.tiktok.com/")
        print("Navigasi ke TikTok berhasil.")
        cookies = driver.get_cookies()
        cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        print("Cookies berhasil diambil.")
        return cookie_str
    except Exception as e:
        print(f"Error saat mengambil cookies: {e}")
        return ""
    finally:
        driver.quit()