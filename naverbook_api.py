# 100개만 받아오기
import urllib.parse
import urllib.request
import json
import mysql.connector


client_id = 'QVAQXj4EupGIr5evnAMr' 
client_secret = 'ueWGuRNLur'

# 검색어
searchText = urllib.parse.quote('크리스마스')

# URL 및 헤더 설정
url = f'https://openapi.naver.com/v1/search/book.json?query={searchText}&display=100'
request = urllib.request.Request(url)    # 네이버 api 요청 준비
request.add_header("X-Naver-Client-Id", client_id)      # 인증 헤더 추가
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)    # 네이버 API 호출
response_body = response.read()     # 실제 응답 데이터
response_body = json.loads(response_body)       # Json -> dict 변환


print(response_body['items'])


connection = mysql.connector.connect(
    host="localhost",
    user='root',
    password='rlaekqls23',
    database='bookdb'
)


cursor = connection.cursor()        # SQL 실행 담당 객체 cursor 생성

sql = "INSERT INTO naver_book (book_title, book_image, author, publisher, isbn, book_description, pub_date) values (%s, %s, %s, %s, %s, %s, %s)"
book_list = response_body['items']
for book_info in book_list:
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

cursor.close()
connection.close()