from PyQt5 import QtWidgets, QtGui, QtCore

class ButtonUpload(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(ButtonUpload, self).__init__()
        widget = QtWidgets.QWidget()
        self.parent = parent
        self.setMinimumHeight(300)
        self.layout = QtWidgets.QGridLayout(widget)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.textLayout = QtWidgets.QHBoxLayout()
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        self.fileIcon = QtWidgets.QPushButton()
        self.fileIcon.setObjectName("historyArrowbtn")
        self.fileIcon.setStyleSheet("background-color: transparent")
        self.fileIcon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fileIcon.setIcon(QtGui.QIcon('assets/upload.svg'))
        self.fileIcon.setIconSize(QtCore.QSize(30, 30))
        self.fileIcon.clicked.connect(self.parent.openFileNameDialog)

        self.text = QtWidgets.QLabel("Drag file here or")
        self.text.setObjectName("textUpload")
        self.textLayout.addWidget(self.text)

        self.text2 = QtWidgets.QLabel("browse")
        self.text2.setObjectName("textUpload2")
        self.textLayout.addWidget(self.text2)

        self.layout.addWidget(self.fileIcon, 0, 0)
        self.layout.addLayout(self.textLayout, 0, 1)

        self.setObjectName("uploadbtn")
        self.setLayout(self.layout)
        self.setMinimumWidth(400)
        self.clicked.connect(self.parent.openFileNameDialog)