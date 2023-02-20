from PyQt5 import QtWidgets, QtGui, QtCore

class ButtonHistory(QtWidgets.QPushButton):
    def __init__(self, file, parent):
        super(ButtonHistory, self).__init__()
        widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(widget)
        self.textLayout = QtWidgets.QVBoxLayout()
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.setMinimumHeight(70)
        self.parent = parent
        fileName = file["name"]
        fileTime = file["time"]

        self.name = QtWidgets.QLabel("")
        self.name.setText(fileName)
        self.name.setObjectName("recentlabel")
        self.textLayout.addWidget(self.name)

        self.time = QtWidgets.QLabel("")
        self.time.setText(fileTime)
        self.time.setObjectName("recentlabelTime")
        self.textLayout.addWidget(self.time)

        self.arrowIcon = QtWidgets.QPushButton()
        self.arrowIcon.setObjectName("historyArrobtn")
        self.arrowIcon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.arrowIcon.setIcon(QtGui.QIcon('assets/arrow.svg'))
        self.arrowIcon.setIconSize(QtCore.QSize(40, 40))
        self.arrowIcon.clicked.connect(lambda: self.parent.navigateToRenderer(fileName))
        

        self.layout.addLayout(self.textLayout, 0, 0)
        self.layout.addWidget(self.arrowIcon, 0, 1)

        self.setObjectName("recentbtn")
        self.setLayout(self.layout)
        self.clicked.connect(lambda: self.parent.navigateToRenderer(fileName))