from PyQt5 import QtWidgets
from widgets.renderer import RendererWidget
from widgets.home import HomeWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl
from utils import saveFileName, getRecentFile, clean
from model.segmentator import Segmentator
from PyQt5.QtGui import QFontDatabase
from widgets.waiting import WaitingWidget
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    begin = pyqtSignal()
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName

    def run(self):
        self.begin.emit()
        self.segmentator = Segmentator(self)
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

        recent_file = getRecentFile()
        if recent_file == fileName:
            return self.setCentralWidget(RendererWidget(self, fileName))
        else:
            clean(True)

        self.worker = Worker(fileName)
        self.worker.start()
        
        self.worker.begin.connect(self.createWaitingWidget)
        self.worker.finished.connect(lambda: self.setCentralWidget(RendererWidget(self, fileName)))
        self.worker.progress.connect(lambda x: self.waitingWidget.label.setText(x))
            
    def createWaitingWidget(self):
        self.waitingWidget = WaitingWidget()
        self.setCentralWidget(self.waitingWidget)

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