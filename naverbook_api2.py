# 있는 만큼 받아오기
import urllib.parse
import urllib.request
import json
import mysql.connector
from datetime import datetime


client_id = 'QVAQXj4EupGIr5evnAMr' 
client_secret = 'ueWGuRNLur'

# 검색어
searchText = urllib.parse.quote('전기자동차')

# URL 및 헤더 설정
url = f'https://openapi.naver.com/v1/search/book.json?query={searchText}&display=1' # 전체 정보를 가져오기 위해 total 먼저 확인
request = urllib.request.Request(url)                   # 네이버 api 요청 준비
request.add_header("X-Naver-Client-Id", client_id)      # 인증 헤더 추가
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)    # 네이버 API 호출
response_body = response.read()               # 실제 응답 데이터
response_body = json.loads(response_body)     # Json -> dict 변환

total_count = response_body['total']          # 전체 검색 결과 개수 확인
start_num = 1
loop_count = total_count // 100 + 1           # 100개씩 끊어서 몇번 반복할 지 계산 (+1은 300(몫) + 20을 위함)
book_list = []                                # 책 데이터 누적할 리스트

for i in range(loop_count):
    url = f'https://openapi.naver.com/v1/search/book.json?query={searchText}&display=100&start={start_num}'
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)      # 인증 헤더 추가
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)    # 네이버 API 호출
    response_body = response.read()               # 실제 응답 데이터
    response_body = json.loads(response_body)     # Json -> dict 변환

    book_list += response_body['items'] # 기존 리스트에 이어붙임
    start_num += 100                   # 다음 구간 요청 (start = j1, 101, 201, ...)

    # 네이버 API start 최대값 1000이기 때문에 1000을 넘으면 break
    if start_num > 1000:
        break

# db연결 객체 생성
connection = mysql.connector.connect(
    host="localhost",
    user='root',
    password='rlaekqls23',
    database='bookdb'
)


cursor = connection.cursor()        # SQL 실행 담당 객체 cursor 생성

sql = "INSERT INTO naver_book (book_title, book_image, author, publisher, isbn, book_description, pub_date) values (%s, %s, %s, %s, %s, %s, %s)"

for book_info in book_list:
    pub_str = book_info.get('pubdate', '')

    if pub_str:
        pub_date = datetime.strptime(pub_str, '%Y%m%d').date()  # datetime
    # 비어있으면
    else:
        pub_date = None

    values = (
        book_info['title'],
        book_info['image'],
        book_info['author'],
        book_info['publisher'],
        book_info['isbn'],
        book_info['description'],
        book_info['pubdate']
    )
    cursor.execute(sql, values)

connection.commit()

# 커서 및 연결 객체 종료 (자원 반납)
cursor.close()
connection.close()