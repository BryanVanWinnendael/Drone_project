from PyQt5 import QtWidgets, QtCore, QtGui

class ButtonSpace(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.layout = QtWidgets.QHBoxLayout()
        
        self.originalButton = QtWidgets.QPushButton("Original")
        self.originalButton.setObjectName("rendererbtn")
        self.originalButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.originalButton.clicked.connect(lambda: self.parent.changeGeometry(self.parent.fileName))

        self.classifiedButton = QtWidgets.QPushButton("Classified")
        self.classifiedButton.setObjectName("rendererbtn")
        self.classifiedButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.classifiedButton.clicked.connect(lambda: self.parent.changeGeometry(self.parent.classified))

        self.daynightSwitch = QtWidgets.QPushButton("Switch Black")
        self.daynightSwitch.setObjectName("rendererbtn")
        self.daynightSwitch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.daynightSwitch.clicked.connect(lambda: self.parent.changeBackground())

        self.layout.addWidget(self.originalButton)
        self.layout.addWidget(self.classifiedButton)
        self.layout.addWidget(self.daynightSwitch)
        self.setLayout(self.layout)