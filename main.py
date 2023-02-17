from PyQt5 import QtWidgets
from widgets.renderer import RendererWidget
from widgets.home import HomeWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl
from utils import saveFileName
from model.segmentator import Segmentator

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        homeWidget = HomeWidget(self)
        self.setCentralWidget(homeWidget)

    # Navigation functions
    def navigateToRenderer(self, fileName):      
        saveFileName(fileName)
        segmentator = Segmentator()
        segmentator.segment(fileName)
        cloudPointWidget = RendererWidget(self, fileName)
        self.setCentralWidget(cloudPointWidget)
        
    
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

    css="style.css"
    with open(css,"r") as fh:
        app.setStyleSheet(fh.read())

    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()