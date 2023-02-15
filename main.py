from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pointCloudScreen import PointCloud_MainWindow
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)

        self.testButton = QtWidgets.QPushButton('Upload file')
        self.testButton.setObjectName("uploadbtn")
        layout.addWidget(self.testButton)

        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label-error")
        layout.addWidget(self.label)

        self.setCentralWidget(central)
        self.setAcceptDrops(True)
        self.testButton.clicked.connect(self.openFileNameDialog)


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
       

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Polygon Files (*.ply)", options=options)
        if fileName and fileName.endswith('.ply'):
            self.launchWindow(fileName)

    def launchWindow(self, fileName=None):
        self.test = PointCloud_MainWindow(fileName)
        self.test.resize(800, 600)
        self.test.backSignal.connect(self.show)
        self.hide()
        self.test.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if (files[0].endswith('.ply') == True):
            print("Opening ply file")
            self.label.clear()
            self.launchWindow(files[0])
        else:
            self.label.setText("Not a ply file")
            print("Not a ply file")


def GUI_Window():
    import sys
    app = QtWidgets.QApplication(sys.argv)

    css="style.css"
    with open(css,"r") as fh:
        app.setStyleSheet(fh.read())

    mainWindow = MainWindow()
    mainWindow.resize(800, 600)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    GUI_Window()