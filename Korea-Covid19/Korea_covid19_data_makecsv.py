# 한국 시도별 코로나19 감염 발생동향 정보 가져오기
import csv
import requests
from bs4 import BeautifulSoup

# 코로나바이러스감염증-19 > 발생동향 > 시도별 발생동향 URL
url = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun="

# CSV 파일 생성
filename = "Korea_covid19_data.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "기준시간 시도명 합계 국내발생 해외유입 확진환자 격리중 격리해제 사망자 발생률(인구10만명당)".split(" ")
writer.writerow(title)

# URL에 GET 요청(request)
responce = requests.get(url)
responce.raise_for_status()

# soup 객체 생성
soup = BeautifulSoup(responce.text, "lxml")

# 데이터 행 가져오기
data_rows = soup.find("table", attrs = {"class" : "num midsize"}).find("tbody").find_all("tr")

# 시간 정보 가져오기
time = soup.find("p", attrs = {"class" : "info"}).find("span").get_text()

# 각 행의 열 값 가져오기
for row in data_rows:
    head_columns = row.find_all("th")
    data_columns = row.find_all("td")
    data = [time] + [column.get_text() for column in head_columns] + [column.get_text() for column in data_columns]
    # csv 파일에 저장
    writer.writerow(data)

