import ctypes

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from model.segmentator import Segmentator
from utils import (cleanData, getRecentFile, getSettings, saveFileName,
                   saveRecentFile)
from widgets.home import HomeWidget
from widgets.renderer import RendererWidget
from widgets.settings import SettingsWidget
from widgets.waiting import WaitingWidget


class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName

    def run(self):
        settings = getSettings()
        
        self.segmentator = Segmentator(self, settings)
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
            saveRecentFile(fileName)

        self.worker = Worker(fileName)
        self.worker.start()
        self.worker.finished.connect(lambda: self.navigateToSegmentation(fileName))
        self.worker.progress.connect(lambda x: self.setLoadingText(x))
    
    def setLoadingText(self, text):
        try: 
            waitingWidgetexist = self.waitingWidget
        except:
            waitingWidgetexist = False
    
        if not waitingWidgetexist:
            self.waitingWidget = WaitingWidget()
            self.setCentralWidget(self.waitingWidget)

        self.waitingWidget.label.setText(text)
    
    def navigateToSegmentation(self, fileName):
        self.waitingWidget = False
        self.setCentralWidget(RendererWidget(self, fileName))

    def navigateToHome(self):
        homeWidget = HomeWidget(self)
        self.setCentralWidget(homeWidget)
    
    def navigateToSettings(self):
        settingsWidget = SettingsWidget(self)
        self.setCentralWidget(settingsWidget)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon('assets/PointCloud.png'))
    
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    css="style.css"
    with open(css,"r") as fh:
        app.setStyleSheet(fh.read())

    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()