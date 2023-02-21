from PyQt5 import QtWidgets, QtGui, QtCore

class ButtonTable(QtWidgets.QPushButton):
    def __init__(self, data, parent):
        super(ButtonTable, self).__init__()
        self.parent = parent
        self.setText("View")
        self.setObjectName("viewButton")
        item_id = data["Segment"]
        fileName = f"data/planes/plane_{item_id}.ply"
        self.clicked.connect(lambda: self.showObject(fileName))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def showObject(self, fileName):
        self.parent.changeGeometry(fileName)