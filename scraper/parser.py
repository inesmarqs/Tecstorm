from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

path = "/usr/local/bin/chromedriver"
url = "https://www.barcodelookup.com/5449000133328"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(path), options=options)
driver.get(url)
time.sleep(2)

with open("barcode_page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print("✅ HTML guardado como 'barcode_page.html'")
