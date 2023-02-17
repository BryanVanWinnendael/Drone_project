from PyQt5 import QtWidgets, QtCore, QtGui
import win32gui
import open3d as o3d
from utils import getFileNames
from widgets.components.resultTable import ResultTable

class RendererWidget(QtWidgets.QWidget):
    def __init__(self, parent, fileName=None):
        super().__init__()
        self.fileName = fileName
        self.parent = parent
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        self.acceptDrops = False
        pcd = o3d.io.read_point_cloud(fileName)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(pcd)      

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        
        self.window = QtGui.QWindow.fromWinId(hwnd)    

        self.windowcontainer = self.createWindowContainer(self.window, widget)
        self.windowcontainer.setMinimumWidth(300)
        self.windowcontainer.setMinimumHeight(300)
        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.clicked.connect(self.parent.navigateToHome)
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))

        self.resultTable = ResultTable(self)
    
        layout.addWidget(self.backButton, 0, 0)
        layout.addWidget(self.windowcontainer, 1, 0)
        layout.addWidget(self.resultTable, 2, 0)

        self.setLayout(layout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)

    def update_vis(self):
        self.vis.poll_events()
        self.vis.update_renderer()

    def changeGeometry(self, fileName):
        self.vis.clear_geometries()
        pcd = o3d.io.read_point_cloud(fileName)
        self.vis.add_geometry(pcd)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)
    
    def mainGeometry(self):
        self.vis.clear_geometries()
        pcd = o3d.io.read_point_cloud(self.fileName)
        self.vis.add_geometry(pcd)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)