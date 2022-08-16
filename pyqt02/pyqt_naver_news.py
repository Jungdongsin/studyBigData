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
        uic.loadUi("./pyqt02/navernews.ui", self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None:
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = qTemplate()
    app.exec_()