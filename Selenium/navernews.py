from selenium import webdriver
from selenium.webdriver.common.by import By    # 요소 선택용
from selenium.webdriver.common.keys import Keys # 키보드 이벤트 조작용
import time

# 1. 크롬 브라우저 실행
path = './chromedriver'                    # 크롬드라이버 경로
service = webdriver.chrome.service.Service(path)     # 서비스 객체 생성
driver = webdriver.Chrome(service=service)   # Chrome 브라우저 실행

driver.get('http://naver.com') # 네이버 메인페이지 이동
time.sleep(1)                  # 1초동안 로딩 기다리기

# 2-1. 검색창에 키워드 입력 + Enter (input id="query")
search_box = driver.find_element(By.ID, 'query')    # id가 'query'인 요소를 찾음
search_box.send_keys('크롤링')                        # 검색어 입력
search_box.send_keys(Keys.RETURN)                   # Enter 누르기
time.sleep(1)                                       # 1초동안 로딩 기다리기

# 2-2. 뉴스 탭 이동
next_btn = driver.find_element(By.CSS_SELECTOR, '.lnb_group ._next .btn')
next_btn.click() # 다음 버튼 클릭
time.sleep(1)

news_btn = driver.find_element(By.CSS_SELECTOR, '.lnb_group a:has(.spnew2.ico_nav_news)')
news_btn.click() # 뉴스 버튼 클릭
time.sleep(1)

# 2-3. 스크롤 내려서 더 많은 기사 로딩
for _ in range(5):
    body = driver.find_element(By.TAG_NAME, "body")       # BODY 태그 선택
    body.send_keys(Keys.END)                              # END -> 맨 아래로 스크롤
    time.sleep(1)

# 3. 데이터 추출
news_cont_els = driver.find_elements(By.CSS_SELECTOR, '.sds-comps-text-type-headline1')

for news_cont_el in news_cont_els:
    parent = news_cont_el.find_element(By.XPATH, "..") # 부모 태그(a 태그 내부의 링크)

    title = news_cont_el.text               # 뉴스 제목
    href = parent.get_attribute('href')     # a 태그의 href 속성값
    print(title, "|", href)

driver.quit() # 브라우저 종료
