from PyQt5 import QtWidgets


class ButtonTable(QtWidgets.QPushButton):
    def __init__(self, data, parent):
        super(ButtonTable, self).__init__()
        self.parent = parent
        self.setText("View")
        name, item_id = data["Segment"].split(" ")
        area = data["Surface area"]
        fileName = f"data/planes/plane_{item_id}.ply"
        self.clicked.connect(lambda: self.showObject(fileName))

    def showObject(self, fileName):
        self.parent.changeGeometry(fileName)
        print(fileName)