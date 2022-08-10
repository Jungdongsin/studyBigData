from cProfile import label
from http.client import ImproperConnectionState
#가장 심플한 PyQt 실행방법
from PyQt5 import QtWidgets as qw

def run():
    app = qw.QApplication([])
    wnd = qw.QMainWindow()
    label = qw.QLabel("Hello PyQt!")
    wnd.setCentralWidget(label)
    wnd.show()
    app.exec_()

if __name__ == "__main__":
    run()


