from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By    # 요소 선택용
from selenium.webdriver.common.keys import Keys # 키보드 이벤트 조작용
import time

# 1. Chrome 브라우저 실행
path = './chromedriver'                          # 크롬 드라이버 파일 경로
service = webdriver.chrome.service.Service(path) # 드라이버 서비스 객체 생성
driver = webdriver.Chrome(service=service)       # 브라우저 실행

# 2 네이버 속 후 '현재상영영화' 검색
driver.get('https://naver.com')
time.sleep(1)

# 2-1. 검색창에 키워드 입력 + Enter (input id="query")
search_box = driver.find_element(By.ID, 'query')    # id가 'query'인 요소를 찾음
search_box.send_keys('현재상영영화')                   # 검색어 입력
search_box.send_keys(Keys.RETURN)                   # Enter 누르기
time.sleep(1)                                       # 1초동안 로딩 기다리기

# 영화정보 div .data_area
movie_items = driver.find_elements(By.CSS_SELECTOR, '.data_area')

# 영화제목 및 상세페이지 링크 출력
for movie_item in movie_items:
    title = movie_item.find_element(By.CSS_SELECTOR, '.title ._text').text
    link = movie_item.find_element(By.CSS_SELECTOR, '.img_box').get_attribute('href')

    print(f"{title} | {link}")

# driver.quit()