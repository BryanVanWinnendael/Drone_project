import os
from PyQt5 import QtCore, QtGui, QtWidgets

from utils import checkDataDirectory, checkZippedData, cleanData, copyDirectory

class ButtonHistory(QtWidgets.QPushButton):
    def __init__(self, file, parent):
        super(ButtonHistory, self).__init__()
        widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(widget)
        self.layout.setObjectName("recentbtn")
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        
        self.textLayout = QtWidgets.QVBoxLayout()
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.setMinimumHeight(70)
        self.parent = parent

        fileName = file["name"]
        fileTime = file["time"]

        try:
            folderPath = file["folderPath"]
        except:
            folderPath = None

        self.fileIcon = QtWidgets.QPushButton()
        self.fileIcon.setObjectName("historyArrowbtn")
        self.fileIcon.setStyleSheet("background-color: transparent")
        self.fileIcon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        if folderPath:
            self.fileIcon.setIcon(QtGui.QIcon('assets/folder.svg'))
        else:
            self.fileIcon.setIcon(QtGui.QIcon('assets/file.svg'))
        self.fileIcon.setIconSize(QtCore.QSize(50, 50))
        self.fileIcon.clicked.connect(lambda: self.parent.navigateToRenderer(fileName))

        self.name = QtWidgets.QLabel("")
        self.name.setText(fileName.split("/")[-1])
        self.name.setObjectName("recentlabelButton")
        self.name.setStyleSheet("background-color: transparent")
        self.textLayout.addWidget(self.name)

        self.time = QtWidgets.QLabel("")
        self.time.setText(fileTime)
        self.time.setStyleSheet("background-color: transparent")
        self.time.setObjectName("recentlabelTimeButton")
        self.textLayout.addWidget(self.time)

        self.layout.addWidget(self.fileIcon, 0, 0)
        self.layout.addLayout(self.textLayout, 0, 1)

        self.setObjectName("recentbtn")
        self.setStyleSheet("background-color: red")
        self.setStyleSheet("QPushButton#recentbtn:hover {background-color: #F6F6F6; text-align: left;}")
        self.setLayout(self.layout)
        self.setMinimumWidth(400)
        if folderPath:
            self.setToolTip(folderPath)
            self.clicked.connect(lambda: self.navigateToRendererFromPreProcessedData(folderPath, fileName))
        else:
            self.setToolTip(fileName)
            self.clicked.connect(lambda: self.navigateToRenderer(fileName))
    
    def navigateToRenderer(self, fileName):
        if os.path.exists(fileName):
            self.parent.navigateToRenderer(fileName)

    def navigateToRendererFromPreProcessedData(self, folderPath, fileName):
        if folderPath.endswith("zip"):
            check = checkZippedData(folderPath)
        else:
            check = checkDataDirectory(folderPath)
        if check:
            cleanData(True)
            copyDirectory(folderPath, "data")
            self.parent.navigateToRendererFromPreProcessedData(folderPath, fileName)