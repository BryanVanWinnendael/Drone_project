from PyQt5 import QtWidgets
from widgets.renderer import RendererWidget
from widgets.home import HomeWidget
from utils import saveFileName, getRecentFile, cleanData
from model.segmentator import Segmentator
from widgets.waiting import WaitingWidget
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtGui
import ctypes

class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName

    def run(self):
        self.segmentator = Segmentator(self)
        self.segmentator.segment(self.fileName)
        self.finished.emit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName("mainWindow")
        self.setWindowTitle("Point cloud renderer")

        homeWidget = HomeWidget(self)
        self.setCentralWidget(homeWidget)

    def navigateToRenderer(self, fileName):   
        saveFileName(fileName)
        recent_file = getRecentFile()

        if recent_file == fileName:
            return self.setCentralWidget(RendererWidget(self, fileName))
        else:
            cleanData(True)

        self.worker = Worker(fileName)
        self.worker.start()
        try:
            self.worker.finished.connect(lambda: self.setCentralWidget(RendererWidget(self, fileName)))
            self.worker.progress.connect(lambda x: self.setLoadingText(x))
        except:
            pass
    
    def setLoadingText(self, text):
        try: 
            waitingWidgetexist = self.waitingWidget
        except:
            waitingWidgetexist = False
    
        if not waitingWidgetexist:
            self.waitingWidget = WaitingWidget()
        self.waitingWidget.label.setText(text)

    def navigateToHome(self):
        homeWidget = HomeWidget(self)
        self.setCentralWidget(homeWidget)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon('assets/drone.png'))
    
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    css="style.css"
    with open(css,"r") as fh:
        app.setStyleSheet(fh.read())

    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()