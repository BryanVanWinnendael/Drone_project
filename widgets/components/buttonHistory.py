from PyQt5 import QtWidgets, QtGui, QtCore

class ButtonHistory(QtWidgets.QPushButton):
    def __init__(self, file, parent):
        super(ButtonHistory, self).__init__()
        self.parent = parent
        fileName = file["name"]
        fileTime = file["time"]
        self.setText(fileName + "\n" + fileTime)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setMinimumHeight(40)
        self.setObjectName("recentbtn")
        self.clicked.connect(lambda: self.parent.navigateToRenderer(fileName))