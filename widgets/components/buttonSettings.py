from PyQt5 import QtCore, QtGui, QtWidgets


class ButtonSettings(QtWidgets.QToolButton):
    def __init__(self, parent):
        super(ButtonSettings, self).__init__()
        self.parent = parent
        self.setIcon(QtGui.QIcon('assets/settings.svg'))
        self.setIconSize(QtCore.QSize(30, 30))
        self.setGeometry(QtCore.QRect(220, 120, 41, 41))
        self.setObjectName("buttonSettings")
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.clicked.connect(lambda: self.parent.navigateToSettings())