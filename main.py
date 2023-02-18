from PyQt5 import QtWidgets
from widgets.renderer import RendererWidget
from widgets.home import HomeWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl
from utils import saveFileName
from model.segmentator import Segmentator
from PyQt5.QtGui import QFontDatabase
from widgets.waiting import WaitingWidget
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName

    def run(self):
        self.progress.emit(0)
        self.segmentator = Segmentator()
        self.segmentator.segment(self.fileName)
        self.finished.emit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        homeWidget = HomeWidget(self)
        self.setCentralWidget(homeWidget)

    # Navigation functions
    def navigateToRenderer(self, fileName):   
        saveFileName(fileName)
        cloudPointWidget = RendererWidget(self, fileName)

        self.worker = Worker(fileName)
        self.worker.start()
        self.setCentralWidget(WaitingWidget())
        self.worker.finished.connect(lambda: self.setCentralWidget(cloudPointWidget))

    
    def navigateToHome(self):
        homeWidget = HomeWidget(self)
        self.setCentralWidget(homeWidget)

    def doRequest(self):   
        url = "https://names.drycodes.com/10"
        req = QNetworkRequest(QUrl(url))
        
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)

    def handleResponse(self, reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            print(str(bytes_string, 'utf-8'))
        else:
            print("Error occured: ", er)
            print(reply.errorString())
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    QFontDatabase.addApplicationFont('assets/fonts/gilroy.otf')

    css="style.css"
    with open(css,"r") as fh:
        app.setStyleSheet(fh.read())

    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()