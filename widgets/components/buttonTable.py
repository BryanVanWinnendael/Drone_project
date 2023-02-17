from PyQt5 import QtWidgets, QtGui, QtCore
import open3d as o3d

class ButtonTable(QtWidgets.QPushButton):
    def __init__(self, data, parent):
        super(ButtonTable, self).__init__()
        self.parent = parent
        self.setText("View")
        name = data["name"]
        item_id = data["id"]
        fileName = f"data/results/{name}_{item_id}.ply"
        self.clicked.connect(lambda: self.showObject(fileName))

    def showObject(self, fileName):
        self.parent.changeGeometry(fileName)
        print(fileName)
        print(type(fileName))
        #pcd = o3d.io.read_point_cloud(fileName)
        #o3d.visualization.draw_geometries([pcd], "", 500, 500)