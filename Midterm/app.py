from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

#Q2-1-1
driver.get("https://docs.python.org/3/tutorial/index.html")

#Q2-1-2
select = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@class='switchers']/div[1]/select[@id='language_select']"))))
select.select_by_value('zh-tw')

#Q2-1-3
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[@lang='zh_TW']")))
print(driver.find_elements(By.XPATH, "//section[@id='the-python-tutorial']/h1")[0].text)
print(driver.find_elements(By.XPATH, "//section[@id='the-python-tutorial']/p")[0].text)


#Q2-2-1
search = driver.find_element(By.XPATH, "//div[@class='inline-search']/form[@class='inline-search']/input[@name='q']")
search.send_keys('class')
search.send_keys(Keys.ENTER)

#Q2-2-2
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='search-results']/ul[@class='search']/li[1]/a")))
print(element.text)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='search-results']/ul[@class='search']/li[2]/a")))
print(element.text)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='search-results']/ul[@class='search']/li[3]/a")))
print(element.text)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='search-results']/ul[@class='search']/li[4]/a")))
print(element.text)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='search-results']/ul[@class='search']/li[5]/a")))
print(element.text)

driver.close()
