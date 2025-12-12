from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymysql

# 1. Chrome 브라우저 실행
path = './chromedriver'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)

driver.get('https://www.hyundai.com/kr/ko/e/vehicles/eco-incentive')
time.sleep(1)

modal_btn = driver.find_element(By.CSS_SELECTOR, '#subsidyAreaSelect')
modal_btn.click()
select_btn = driver.find_element(By.CSS_SELECTOR, '#subsidyAreaSelect ')
select_btn.click()

time.sleep(10)