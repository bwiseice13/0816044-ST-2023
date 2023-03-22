from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.nycu.edu.tw/")

driver.maximize_window()

button = driver.find_element(By.XPATH, '//a[@title="新聞"]')
button.click()

button = driver.find_elements(By.XPATH, "//ul[@class='su-posts su-posts-list-loop']/li/a")[0]
button.click()

print(driver.find_elements(By.XPATH, "//header[@class='entry-header clr']/h1")[0].text)
print(driver.find_elements(By.XPATH, "//div[@class='entry-content clr']")[0].text)

driver.switch_to.new_window("tab")
driver.get("https://www.google.com")

search = driver.find_element(By.NAME, 'q')
search.send_keys('0816044')
search.send_keys(Keys.ENTER)

# try:
results = driver.find_elements(By.XPATH, "//div[contains(@class, 'g')]/div[1]//h3")
print(results[1].text)

driver.close()
