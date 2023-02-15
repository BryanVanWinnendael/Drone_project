from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import win32gui
from cloudPointWidget import CloudPointWidget
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        nav_cloud_button = navCloudPointWidget(self)
        nav_cloud_button.button.clicked.connect(self.getCloudPointWidget)
        self.central_widget.addWidget(nav_cloud_button)

    def getCloudPointWidget(self):
        cloud_point_widget = CloudPointWidget(self)
        self.central_widget.addWidget(cloud_point_widget)
        self.central_widget.setCurrentWidget(cloud_point_widget)

class navCloudPointWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(navCloudPointWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton('Go to CloudPointWidget')
        layout.addWidget(self.button)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()