from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


# 클래스 OOP
class qTemplate(QWidget):
    #생성자
    def __init__(self) -> None:
    #-> None: return이 없다는 것(원래 생성자는 return이 없어서 none이 기본이다)
        super().__init__()
        uic.loadUi("./pyqt02/t_task.ui", self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.setGeometry(300, 100, 640, 400) #창 위치(ax:가로, ay:세로) 창 크기(aw:너비, ah:높이)
        self.setWindowTitle("QPushbutton 예제!!")
        self.show()

    def addControls(self) -> None:
        self.btn1 = QPushButton()
        self.btn1.clicked.connect(self.btn1_clicked) # 시그널 연결

    # event = signal(python)
    def btn1_clicked(self):
        self.label.setText("메시지 : btn1 버튼 클릭!!!")
        QMessageBox.critical(self, "signal", "btn1_clicked")   #에러창

if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = qTemplate()
    app.exec_()