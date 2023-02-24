from PyQt5 import QtWidgets, QtCore, QtGui
import open3d as o3d
from widgets.components.resultTable import ResultTable
from widgets.components.resultTopBar import ResultTopBar
from widgets.components.buttonSpace import ButtonSpace
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import csv
import win32gui

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
        
        self.pcd = o3d.io.read_point_cloud(fileName)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(self.pcd)    

        self.classified_pcd = o3d.io.read_point_cloud(self.classified)
        self.classified_pcd_downscaled = o3d.io.read_point_cloud(self.classified)
        self.classified_pcd_downscaled.voxel_down_sample(voxel_size=0.5)
        self.classified_pcd_downscaled.paint_uniform_color([0.5, 0.5, 0.5])

        self.original_view = self.vis.get_view_control().convert_to_pinhole_camera_parameters() 
        self.canResetOriginalView = True

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        
        self.window = QtGui.QWindow.fromWinId(hwnd)    

        self.windowcontainer = self.createWindowContainer(self.window, widget)
        self.windowcontainer.setMinimumWidth(300)
        self.windowcontainer.setMinimumHeight(300)

        self.topBar = ResultTopBar(self.fileName, self.parent)
        self.buttonSpace = ButtonSpace(self)
        self.resultTable = ResultTable(self, self.data)

        total_area = sum([float(info["Surface area"]) for info in self.data])
        self.area_label = QtWidgets.QLabel(f"Total area: {total_area} m²")
        self.area_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.area_label.setAlignment(Qt.AlignCenter)
        self.area_label.setMaximumHeight(50)
    
        self.tableAndButtonSpace = QtWidgets.QWidget()
        self.tableAndButtonsLayout = QtWidgets.QVBoxLayout()

        self.tableAndButtonsLayout.addWidget(self.buttonSpace)
        self.tableAndButtonsLayout.addWidget(self.area_label)
        self.tableAndButtonsLayout.addWidget(self.resultTable)
        self.tableAndButtonSpace.setLayout(self.tableAndButtonsLayout)

        self.splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.windowcontainer)
        self.splitter.addWidget(self.tableAndButtonSpace)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 5)
        self.splitter.setSizes([100,200])
       
        layout.addWidget(self.topBar, 0, 0)
        layout.addWidget(self.splitter, 1, 0)

        self.setLayout(layout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)

    def update_vis(self):
        self.vis.poll_events()
        self.vis.update_renderer()

    def changeGeometry(self, fileName):
        if fileName != self.fileName and self.canResetOriginalView:
            self.original_view = self.vis.get_view_control().convert_to_pinhole_camera_parameters()
            self.canResetOriginalView = False

        self.vis.clear_geometries()

        pcds = []

        if fileName == self.fileName:
            pcds.append(self.pcd)

        elif fileName == self.classified:
            pcds.append(self.classified_pcd)
        else:
            cloud = o3d.io.read_point_cloud(fileName)
            print(cloud.points)
            pcds.append(cloud)
            pcds.append(self.classified_pcd_downscaled)

        for pcd in pcds:
            self.vis.add_geometry(pcd)      
        self.vis.reset_view_point(True)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)

    def changeViewToOriginal(self):
        ctr = self.vis.get_view_control()
        ctr.convert_from_pinhole_camera_parameters(self.original_view)
        self.canResetOriginalView = True
    
    def resetOriginalView(self, *args):
        self.vis.reset_view_point(True)
        self.canResetOriginalView = True
        self.original_view = self.vis.get_view_control().convert_to_pinhole_camera_parameters()

    def changeBackground(self):
        opt = self.vis.get_render_option()
        
        if self.night:
            opt.background_color = np.asarray([255, 255, 255])
            self.night = False
            self.buttonSpace.daynightSwitch.setText("Switch Black")
        else:
            opt.background_color = np.asarray([0, 0, 0])
            self.night = True
            self.buttonSpace.daynightSwitch.setText("Switch White")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)

def removePointsFromPointCloud(pointcloud, points_to_remove):
    pc_points = np.asarray(pointcloud.points)
    points_to_mask = np.asarray(points_to_remove)

    indexes = [i for i in range(len(pc_points)) if np.any(np.all(pc_points[i] == points_to_mask, axis=1))]

    mask = np.ones(len(pc_points), dtype=bool)
    mask[indexes] = False
    return pc_points[mask]