import requests                             # HTML 요청
from bs4 import BeautifulSoup               # 정적 페이지 파싱
from urllib.request import urlretrieve      # url에서 이미지 저장시에 사용
from datetime import datetime               # 현재시간 (이미지 경로에 사용)

class MusicEntry:
    def __init__(self, title, artist, img_path):
        self.title = title
        self.artist = artist
        self.img_path = img_path
    
    def __repr__(self): # 객체에 대한 설명을 해주는 매직메소드
        return f"🎵 {self.artist}의 {self.title} | {self.img_path}"
    
# 1. Bugs 실시간 차트 페이지 요청
response = requests.get('https://www.kia.com/kr/customer-service/center/faq') # GET 요청 -> html응답이 옴

# print(response) # 200이면 올바르게 온 것

# 2. BeautifulSoup으로 html 파싱
bs = BeautifulSoup(response.text, 'html.parser') # html 분석 객체 생성
# print(bs.prettify()) # bs를 html 트리형식에 맞게 가져오기

# 3. 곡 리스트 선택 (table.list.trackList.byChart > tbody > tr)
track_list = bs.select('table.list.trackList.byChart tbody tr')

# print(track_list) # 리스트 잘 가져오는지 확인
# print(track_list[0])

# 4. 1위 ~ 끝까지의 순위 데이터 저장 -> 순위를 지정하고싶으면 enumerate(track_list[:30])
result_list = []

# title = p.title a
# artist = p.artist a
# img = a.thumbnail img태그의 href 속성값
for i, song in enumerate(track_list):
    title = song.select_one('p.title a').text.strip()      # 제목 추출
    artist = song.select_one('p.artist a').text.strip()    # 가수명 추출
    img_src = song.select_one('a.thumbnail img')['src']        # img 태그의 src 속성 추출

    filename = f"BeautifulSoup/img/{datetime.now().strftime('%y%m%d_%H%M%S')}_{i+1}.jpg" # 이미지의 파일명

    urlretrieve(img_src, filename) # 이미지 저장

    # MesicEntry 객체 생성 후 리스트에 추가
    music_entry = MusicEntry(title, artist, filename)
    result_list.append(music_entry)

# 5. 최종 출력
for result in result_list:
    print(result)