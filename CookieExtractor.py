from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")

service = Service("C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://dotic.ir")
time.sleep(5)

cookies = driver.get_cookies()
for cookie in cookies:
    print(cookie)

driver.quit()
