from PyQt5 import QtWidgets, QtGui, QtCore

class ButtonTable(QtWidgets.QPushButton):
    def __init__(self, data, parent, rgb):
        super(ButtonTable, self).__init__()
        self.parent = parent
        self.disabled = False
        self.rgb = rgb
        self.setText("View")
        self.setObjectName("viewButton")
        item_id = data["Segment"]
        fileName = f"data/planes/plane_{item_id}.ply"
        self.clicked.connect(lambda: self.showObject(fileName))
        
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.parent.loadingSegment.connect(lambda: self.setDisabled(True))
        self.parent.finishedLoadingSegment.connect(lambda: self.setDisabled(False))
        self.setStyleSheet(f"background-color: rgb({self.rgb[0]}, {self.rgb[1]}, {self.rgb[2]}); color: rgb(255, 255, 255);")

    def setDisabled(self, bool):
        self.disabled = bool

        if self.disabled:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def showObject(self, fileName):
        if not self.disabled:
            self.parent.changeGeometry(fileName)
    
