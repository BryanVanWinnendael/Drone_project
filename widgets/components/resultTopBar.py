from PyQt5 import QtWidgets, QtCore, QtGui

class ResultTopBar(QtWidgets.QWidget):
    def __init__(self, fileName, parent):
        super(ResultTopBar, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.parent = parent
        self.fileName = fileName

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.clicked.connect(self.parent.navigateToHome)
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))

        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setMaximumHeight(25)

        name = fileName.split("/")[-1].split(".")[0]
        self.nameLabel.setText(name)
        self.nameLabel.setObjectName("recentlabel")
        self.layout.addWidget(self.backButton)
        self.layout.addWidget(self.nameLabel)

        self.setLayout(self.layout)