from PyQt5 import QtWidgets, QtGui, QtCore

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

        self.fileIcon = QtWidgets.QPushButton()
        self.fileIcon.setObjectName("historyArrowbtn")
        self.fileIcon.setStyleSheet("background-color: transparent")
        self.fileIcon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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
        self.setToolTip(fileName)
        self.clicked.connect(lambda: self.parent.navigateToRenderer(fileName))