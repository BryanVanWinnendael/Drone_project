from PyQt5 import QtWidgets, QtCore, QtGui
import win32gui
import open3d as o3d
from widgets.components.resultTable import ResultTable
from widgets.components.resultTopBar import ResultTopBar
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import csv

class RendererWidget(QtWidgets.QWidget):
    def __init__(self, parent, fileName=None):
        super().__init__()
        self.fileName = fileName
        self.classified = "data/results/result-classified.ply"
        self.parent = parent
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        self.acceptDrops = False       
        self.night = False

        file = open("data/results/output.csv", "r")
        self.data = list(csv.DictReader(file, delimiter=","))
        file.close()
        
        pcd = o3d.io.read_point_cloud(fileName)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(pcd)      

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        
        self.window = QtGui.QWindow.fromWinId(hwnd)    

        self.windowcontainer = self.createWindowContainer(self.window, widget)
        self.windowcontainer.setMinimumWidth(300)
        self.windowcontainer.setMinimumHeight(300)

        self.topBar = ResultTopBar(self.fileName, self.parent)

        self.buttonSpace = QtWidgets.QWidget()

        self.buttonSpaceLayout = QtWidgets.QHBoxLayout()

        self.originalButton = QtWidgets.QPushButton("Original")
        self.originalButton.setObjectName("backbtn")
        self.originalButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.originalButton.clicked.connect(lambda: self.changeGeometry(self.fileName))

        self.classifiedButton = QtWidgets.QPushButton("Classified")
        self.classifiedButton.setObjectName("backbtn")
        self.classifiedButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.classifiedButton.clicked.connect(lambda: self.changeGeometry(self.classified))

        self.daynightSwitch = QtWidgets.QPushButton("Switch Black")
        self.daynightSwitch.setObjectName("backbtn")
        self.daynightSwitch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.daynightSwitch.clicked.connect(lambda: self.changeBackground())

        self.buttonSpaceLayout.addWidget(self.originalButton)
        self.buttonSpaceLayout.addWidget(self.classifiedButton)
        self.buttonSpaceLayout.addWidget(self.daynightSwitch)
        self.buttonSpace.setLayout(self.buttonSpaceLayout)

        self.resultTable = ResultTable(self, self.data)
    
        self.tableAndButtonSpace = QtWidgets.QWidget()
        self.tableAndButtonsLayout = QtWidgets.QVBoxLayout()

        self.tableAndButtonsLayout.addWidget(self.buttonSpace)
        self.tableAndButtonsLayout.addWidget(self.resultTable)
        self.tableAndButtonSpace.setLayout(self.tableAndButtonsLayout)

        self.splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.windowcontainer)
        self.splitter.addWidget(self.tableAndButtonSpace)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 5)

        self.splitter.setSizes([100,200])

        total_area = sum([float(info["Surface area"]) for info in self.data])
        self.area_label = QtWidgets.QLabel(f"Total area: {total_area} m²")
        self.area_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.area_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.topBar, 0, 0)
        layout.addWidget(self.windowcontainer, 1, 0)
        layout.addWidget(self.area_label, 2, 0)
        layout.addWidget(self.splitter, 3, 0)

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
        self.vis.reset_view_point(True)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)

    def changeBackground(self):
        opt = self.vis.get_render_option()
        
        if self.night:
            opt.background_color = np.asarray([255, 255, 255])
            self.night = False
            self.daynightSwitch.setText("Switch Black")
        else:
            opt.background_color = np.asarray([0, 0, 0])
            self.night = True
            self.daynightSwitch.setText("Switch White")

        

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)