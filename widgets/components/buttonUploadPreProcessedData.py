from PyQt5 import QtWidgets, QtGui, QtCore

class ButtonUploadPreProcessedData(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(ButtonUploadPreProcessedData, self).__init__()
        widget = QtWidgets.QWidget()
        self.parent = parent
        self.setMinimumHeight(100)
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

        self.text = QtWidgets.QLabel("Open pre-processed data")
        self.text.setObjectName("textUpload")
        self.textLayout.addWidget(self.text)

        self.layout.addWidget(self.fileIcon, 0, 0)
        self.layout.addLayout(self.textLayout, 0, 1)

        self.setObjectName("uploadbtn")
        self.setLayout(self.layout)
        self.setMinimumWidth(400)
        self.clicked.connect(self.parent.openDirectoryDialog)

    def setError(self):
        self.text.setText("Error: File is not a valid data directory")
        self.text2.setText("")
        self.text.setStyleSheet("color: #b22222")
        self.text2.setStyleSheet("color: #b22222")
        self.setStyleSheet("border-color: #b22222")
    
    def setNormal(self):
        self.text.setText("Drag folder here or")
        self.text2.setText("browse")
        self.text.setStyleSheet("color: black")
        self.text2.setStyleSheet("color: #249ea7")
        self.setStyleSheet("border-color: #d7e1fc")