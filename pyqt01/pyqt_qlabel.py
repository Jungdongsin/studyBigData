
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
        self.addControls()
        self.setGeometry(300, 100, 640, 400) #창 위치(ax:가로, ay:세로) 창 크기(aw:너비, ah:높이)
        self.setWindowTitle("*QLabel*")
        self.show()
    
    def addControls(self) -> None:
        self.setWindowIcon(QIcon("./pyqt01/image/lion.png")) #윈도우 아이콘 지정
        label1 = QLabel("Label1", self)
        label2 = QLabel("Label2", self)
        label1.setStyleSheet(
            ("border-width: 3px;" #선 두께
            "border-style: solid;" #선 종류
            "border-color: blue;" #색
            "image: url(./pyqt01/image/image1.png)") #상대경로 불가
        )
        label2.setStyleSheet(
            ("border-width: 3px;" #선 두께
            "border-style: dot-dot-dash;" #선 종류
            "border-color: red;" #색
            "image: url(./pyqt01/image/image2.png)") #상대경로 불가
        )


        box = QHBoxLayout() #H는 수평/ V는 수직
        box.addWidget(label1)
        box.addWidget(label2)

        self.setLayout(box)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = qTemplate()
    app.exec_()
