import sys
from PyQt5.QtWidgets import QApplication, QWidget
 
# 클래스 OOP
class qTemplate(QWidget):
    #생성자
    def __init__(self) -> None:
    #-> None: return이 없다는 것(원래 생성자는 return이 없어서 none이 기본이다)
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(300, 100, 640, 400) #창 위치(ax:가로, ay:세로) 창 크기(aw:너비, ah:높이)
        self.setWindowTitle("QTemplate!!")
        self.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = qTemplate()
    app.exec_()