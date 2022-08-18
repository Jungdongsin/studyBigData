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
import pandas as pd # csv 저장용


# 클래스 OOP
class qTemplate(QWidget):
    start = 1   # api호출할 때 시작하는 데이터 번호
    max_display = 100   # 한페이지에 나올 데이터 수
    saveResult = [] # 저장할때 담을 데이터(딕셔너리 리스트) -> DataFrame

    #생성자
    def __init__(self) -> None:
    #-> None: return이 없다는 것(원래 생성자는 return이 없어서 none이 기본이다)
        super().__init__()
        uic.loadUi("./pyqt03/navernews_2.ui", self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None:  # 위젯 정의, 이벤트(시그널) 처리
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked) # 검색할때 엔터치면 검색해주는거(원래는 마우스로 "검색"클릭해야했음)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)\
        
        # 22.08.18 추가버튼 이벤트(시그널) 확장
        self.btnNext.clicked.connect(self.btnNextClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)

    def btnNextClicked(self) -> None: #start=1 display=10이면, 다음 페이지는 start=11임
        self.start = self.start + self.max_display
        self.btnSearchClicked()

    def btnSaveClicked(self) -> None:
        if len(self.saveResult) > 0:
            df = pd.DataFrame(self.saveResult)
            df.to_csv(f"./pyqt03/{self.txtSearch.text()}_뉴스검색결과.csv", encoding="utf-8", index=True)

        QMessageBox.information(self, "저장", "저장완료!")
        
        # 저장 후 모든 변수 초기화(초기화 안할시 다음에 할때 섞일 가능성있음)
        self.saveResult = []
        self.start = 1
        self.txtSearch.setText("")
        self.lblStatus.setText("Data : ")
        self.lblStatus2.setText("저장할데이터 > 0개")
        self.tblResult.setRowCount(0)
        self.btnNext.setEnabled(True)


    def tblResultSelected(self) -> None: # 링크나 제목 누르면 웹사이트로 연결되는거
        selected = self.tblResult.currentRow()   # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 1).text()
        webbrowser.open(link)
        
    def btnSearchClicked(self) -> None: # 슬롯(이벤트핸들러)
        jsonResult = []
        totalResult = []
        keyword = "news"
        search_word = self.txtSearch.text()

        
        #QMessageBox.information(self, "결과", search_word)
        jsonResult = self.getnaverSearch(keyword, search_word, self.start, self.max_display)
        #print(jsonResult)

        for post in jsonResult["items"]:
            totalResult.append(self.getPostData(post))
        #print(totalResult)
        self.makeTable(totalResult) #qtable widgetd에 데이터를 보여주는 역할
        
        # saveResult 값 할당, lblStatus /2 상태값을 표시
        total = jsonResult["total"]
        curr = self.start + self.max_display - 1

        self.lblStatus.setText(f"Data : {curr} / {total}")
        
        # saveResult 변수에 저장할 데이터를 복사
        for post in totalResult:
            self.saveResult.append(post[0])

        self.lblStatus2.setText(f"저장할데이터 > {len(self.saveResult)}개")
        
        if curr >= 1000:
            self.btnNext.setDisabled(True)  # 다음버튼 비활성화
        else:
            self.btnNext.setEnabled(True)   # 다음버튼 활성화
        
        
    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result)) # displayCount에 따라서 변경
        self.tblResult.setHorizontalHeaderLabels(["기사제목", "뉴스링크",])
        self.tblResult.setColumnWidth(0, 350)
        self.tblResult.setColumnWidth(1, 100)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # readonly
        # 테이블 위젯 설정
        
        i = 0
        for item in result:
            title = self.strip_tag(item[0]["title"])
            link = item[0]["originallink"]
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(link))
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
        title = self.strip_tag(post["title"])   #모든 곳에서 html태그 제거
        description = self.strip_tag(post["description"])
        originallink = post["originallink"]
        link = post["link"]
        pubDate = post["pubDate"]

        temp.append({"title": title,
                     "description" : description,
                     "originallink" : originallink,
                     "link" : link,
                     "pubDate" : pubDate}) #220818 pubDate빠진거 추가

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