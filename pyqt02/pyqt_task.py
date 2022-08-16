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
        uic.loadUi("./pyqt02/ttask.ui", self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None:
        #self.btn1 = QPushButton()
        self.btnStart.clicked.connect(self.btn1_clicked) # 시그널 연결

    # event = signal(python)
    def btn1_clicked(self):
        self.txbLog.append("실행~")
        self.pgbTask.setRange(0, 999999)
        for i in range(0,1000000):  #응답없음 발생
            print(f"출력 : {i}")
            self.pgbTask.setValue(i)
            self.txbLog.append(f"출력 > {i}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = qTemplate()
    app.exec_()