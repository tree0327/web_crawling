import requests

params = {
    "key": "33d28a024ade6c377ded6e2b3b69bcd4",
    "targetDt": "20251207"
}

url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"

# API 요청
response = requests.get(url, params=params)

# 결과 출력
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")

data = response.json()
movie_list = data['boxOfficeResult']['dailyBoxOfficeList']

for i in range(len(movie_list)):
    movie_name = movie_list[i]['movieNm']
    print(movie_name)