import imp
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

# 클래스 OOP
class qTemplate(QWidget):
    #생성자
    def __init__(self) -> None:
    #-> None: return이 없다는 것(원래 생성자는 return이 없어서 none이 기본이다)
        super().__init__()
        self.initUI()

    # 화면 정의를 위해 사용자 함수
    def initUI(self) -> None:
        self.setGeometry(300, 100, 640, 400) #창 위치(ax:가로, ay:세로) 창 크기(aw:너비, ah:높이)
        self.setWindowTitle("QFont!!")
        self.text = "What a wonderful world~"
        self.show()
    
    def paintEvent(self, event) -> None:
        paint = QPainter()
        paint.begin(self)
        # 그리는 함수 추가
        self.drawText(event, paint)
        paint.end()

    # 텍스트 그리기 위한 사용자함수
    def drawText(self, event, paint):
        paint.setPen(QColor(50,50,50))
        paint.setFont(QFont("NanumGothic", 20))
        paint.drawText(105,100, "HELL WORLD~!")
        paint.setPen(QColor(0,250,10))
        paint.setFont(QFont("Impact", 10))
        paint.drawText(event.rect(),Qt.AlignCenter,self.text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = qTemplate()
    app.exec_()
