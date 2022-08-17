# pyQt
from ast import keyword
from functools import total_ordering
from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#네이버 openApi
from urllib.parse import quote
import urllib.request
import json
import webbrowser


# 클래스 OOP
class qTemplate(QWidget):
    #생성자
    def __init__(self) -> None:
    #-> None: return이 없다는 것(원래 생성자는 return이 없어서 none이 기본이다)
        super().__init__()
        uic.loadUi("./pyqt02/navernews.ui", self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None:  # 위젯 정의, 이벤트(시그널) 처리
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked) # 검색할때 엔터치면 검색해주는거(원래는 마우스로 "검색"클릭해야했음)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)
        
        
    def tblResultSelected(self) -> None: # 링크나 제목 누르면 웹사이트로 연결되는거
        selected = self.tblResult.currentRow()   # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 2).text() # -> movie : 1 -> 2
        webbrowser.open(link)
        
    def btnSearchClicked(self) -> None: # 슬롯(이벤트핸들러)
        jsonResult = []
        totalResult = []
        keyword = "movie"
        search_word = self.txtSearch.text()
        display_count = 100
        
        QMessageBox.information(self, "결과", search_word)
        jsonResult = self.getnaverSearch(keyword, search_word, 1, display_count)
        #print(jsonResult)
        for post in jsonResult["items"]:
            totalResult.append(self.getPostData(post))
        #print(totalResult)
        self.makeTable(totalResult) #qtable widgetd에 데이터를 보여주는 역할
        return

    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(3) # -> movie: 2(news) -> 3(movie)
        self.tblResult.setRowCount(len(result)) # displayCount에 따라서 변경
        self.tblResult.setHorizontalHeaderLabels(["영화제목", "상영년도", "뉴스링크"]) # -> movie : 제목변경
        self.tblResult.setColumnWidth(0, 250)
        self.tblResult.setColumnWidth(1, 100)
        self.tblResult.setColumnWidth(2, 100)   # -> movie : 세번재 컬럼 길이
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # readonly
        # 테이블 위젯 설정
        
        i = 0
        for item in result:
            title = self.strip_tag(item[0]["title"])
            subtitle = self.strip_tag(item[0]["subtitle"])
            pubDate = item[0]["pubDate"]
            link = item[0]["link"] # -> movie : originallink -> link
            self.tblResult.setItem(i, 0, QTableWidgetItem(f"{title} / {subtitle}")) #-> movie : subtitle 추가
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate)) #-> movie : pubDate 추가
            self.tblResult.setItem(i, 2, QTableWidgetItem(link)) # -> movie : 1->2
            i += 1

    def strip_tag(self, title): # html 태그를 없애주는 함수
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')
        ret = ret.replace('&quot;', '"') 
        ret = ret.replace('&qpos;', "'")    
        ret = ret.replace('&amo;', '&')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')
        return ret


    def getPostData(self, post): #선택된것만 뽑아 출력
        temp = []
        title = post["title"]
        subtitle = post["subtitle"] #-> movie : subtilte 추가
        link = post["link"] # -> movie : originallink -> link
        pubDate = post["pubDate"]

        temp.append({"title": title,
                     "subtitle" : subtitle,  # -> movie : subtilte 추가
                     "pubDate" : pubDate, #-> movie : pubDate 필요해서 추가
                     "link" : link})

        return temp


    # 네이버API 크롤링 함수
    def getnaverSearch(self, keyword, search, start, display): # 돌려주는 값이 있어서 -> None이 아님
        url = f"https://openapi.naver.com/v1/search/{keyword}.json" \
            f"?query={quote(search)}&start={start}&display={display}" #qoute를 사용하지 않으면 검색이 안됨
        print(url)
        req = urllib.request.Request(url)
        # 네이버 인증 추가
        req.add_header("X-Naver-Client-Id", "JJLJeMkKYWKG3IW4fcPD")
        req.add_header("X-Naver-Client-Secret", "jRTJd32ESR")
        
        res = urllib.request.urlopen(req)
        if res.getcode() == 200:
            print("URL request suceed")
        else:
            print("URL request failed")

        ret = res.read().decode("utf-8")
        if ret == None:
            return None
        else:
            return json.loads(ret)
                    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = qTemplate()
    app.exec_()