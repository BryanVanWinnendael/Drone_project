from PyQt5 import QtCore, QtGui, QtWidgets


class ButtonTable(QtWidgets.QPushButton):
    def __init__(self, data, parent, rgb):
        super(ButtonTable, self).__init__()
        self.parent = parent
        self.rgb = rgb
        self.setText("View")
        self.setObjectName("viewButton")
        item_id = data["Segment"]
        fileName = f"data/planes/plane_{item_id}.ply"
        self.clicked.connect(lambda: self.showObject(fileName))
        
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet(f"background-color: rgb({self.rgb[0]}, {self.rgb[1]}, {self.rgb[2]}); color: rgb(255, 255, 255);")

    def showObject(self, fileName):
        self.parent.changeGeometry(fileName)
    
