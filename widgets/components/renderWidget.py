import numpy as np
import open3d as o3d
import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from widgets.waiting import WaitingWidget


class Worker(QThread):
    finished = pyqtSignal(o3d.cpu.pybind.geometry.PointCloud)
    begin = pyqtSignal()

    def __init__(self, fileName, newFileName):
        super().__init__()
        self.fileName = fileName
        self.newFileName = newFileName
        self.classified = "data/results/result-classified.ply"

    def run(self):
        self.begin.emit()
        pcd = o3d.io.read_point_cloud(self.newFileName)
        if self.newFileName not in [self.fileName, self.classified]:
            original_pcd = o3d.io.read_point_cloud(self.fileName)
            if len(np.asarray(original_pcd.points)) > 200000:
                original_pcd = original_pcd.voxel_down_sample(voxel_size=0.1)
            original_points = removePointsFromPointCloud(original_pcd, pcd.points)
            original_colors = np.full((len(original_points), 3), [0.5, 0.5, 0.5])
            new_points = np.asarray(pcd.points)
            new_colors = np.asarray(pcd.colors)
            pcd.points = o3d.utility.Vector3dVector(np.concatenate((original_points, new_points)))
            pcd.colors = o3d.utility.Vector3dVector(np.concatenate((original_colors, new_colors)))
        self.finished.emit(pcd)

class RenderWidget(QtWidgets.QWidget):
    def __init__(self, fileName, parent):
        super(RenderWidget, self).__init__()
        self.fileName = fileName
        self.widget = QtWidgets.QWidget()
        self.parent = parent
        self.classified = "data/results/result-classified.ply"
        self.night = False

        pcd = o3d.io.read_point_cloud(fileName)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(pcd)     

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        self.window = QtGui.QWindow.fromWinId(hwnd)    

        self.Vbox = QtWidgets.QVBoxLayout(self)
        self.windowcontainer = self.parent.createWindowContainer(self.window, self.widget)
        self.windowcontainer.setMinimumWidth(300)
        self.windowcontainer.setMinimumHeight(300)
        self.Vbox.addWidget(self.windowcontainer)

        self.timer = QtCore.QTimer(self.parent)
        self.timer.timeout.connect(self.update_vis)
        self.timer.start(1)

        self.setLayout(self.Vbox)

    def update_vis(self):
        self.vis.poll_events()
        self.vis.update_renderer()
    
    def changeGeometry(self, mewFileName):
        self.worker = Worker(self.fileName, mewFileName)
        self.worker.start()
        self.worker.begin.connect(lambda: self.parent.loadingSegment.emit())
        self.worker.finished.connect(lambda pcd: self.setNewPcd(pcd))
  
    def setNewPcd(self, pcd):
        self.windowcontainer.show()
        original_view = self.vis.get_view_control().convert_to_pinhole_camera_parameters() 
        self.vis.clear_geometries()
        self.vis.add_geometry(pcd)
        ctr = self.vis.get_view_control()
        ctr.convert_from_pinhole_camera_parameters(original_view)
        self.parent.finishedLoadingSegment.emit()

    def changeBackground(self):
        opt = self.vis.get_render_option()
        
        if self.night:
            opt.background_color = np.asarray([255, 255, 255])
            self.night = False
            self.parent.buttonSpace.daynightSwitch.setText("Switch Black")
        else:
            opt.background_color = np.asarray([0, 0, 0])
            self.night = True
            self.parent.buttonSpace.daynightSwitch.setText("Switch White")

def removePointsFromPointCloud(pointcloud, points_to_remove):
    pc_points = np.asarray(pointcloud.points)
    points_to_mask = np.asarray(points_to_remove)

    indexes = [i for i in range(len(pc_points)) if np.any(np.all(pc_points[i] == points_to_mask, axis=1))]

    mask = np.ones(len(pc_points), dtype=bool)
    mask[indexes] = False
    return pc_points[mask]