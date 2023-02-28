import numpy as np
import open3d as o3d    
import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets

class WorkerCloseScreen(QtCore.QThread):
    def __init__(self, parent=None):
        super(WorkerCloseScreen, self).__init__(parent)
        self.parent = parent

    def run(self):
        on = True
        while on:
            hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D - free view")
            if hwnd != 0:
                on = False
                self.parent.vis.close()

class RenderWidget(QtWidgets.QWidget):
    def __init__(self, fileName, parent):
        super(RenderWidget, self).__init__()
        self.fileName = fileName
        self.widget = QtWidgets.QWidget()
        self.parent = parent
        self.classified = "data/results/result-classified.ply"
        self.night = False

        self.pcd = o3d.io.read_point_cloud(fileName)
        self.vis = o3d.visualization.VisualizerWithVertexSelection()
        worker = WorkerCloseScreen(self)
        worker.start()

        self.vis.create_window()
        self.vis.add_geometry(self.pcd)
        self.vis.run()

        win32gui.CloseWindow(win32gui.FindWindowEx(0, 0, None, "Open3D - free view"))

        self.classified_pcd = o3d.io.read_point_cloud(self.classified)
        self.classified_pcd_downscaled = o3d.io.read_point_cloud(self.classified)
        self.classified_pcd_downscaled.voxel_down_sample(voxel_size=0.001)
        self.classified_pcd_downscaled.paint_uniform_color([0.5, 0.5, 0.5])

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D - free view")
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
    
    def changeGeometry(self, newFileName):
        original_view = self.vis.get_view_control().convert_to_pinhole_camera_parameters() 
       
        self.vis.clear_geometries()

        if newFileName == self.fileName:
            self.vis.add_geometry(self.pcd)

        elif newFileName == self.classified:
            self.vis.add_geometry(self.classified_pcd)
        else:
            self.vis.add_geometry(o3d.io.read_point_cloud(newFileName))
            self.vis.add_geometry(self.classified_pcd_downscaled)

        ctr = self.vis.get_view_control()
        ctr.convert_from_pinhole_camera_parameters(original_view)
  
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
    
    def clearSelectedPoints(self):
        self.vis.clear_picked_points()
        self.vis.update_renderer()
    
    def mergepoints(self):
        picked_points = self.vis.get_picked_points()
        print(picked_points)

    def updateClassified(self):
        self.classified_pcd = o3d.io.read_point_cloud(self.classified)
        self.changeGeometry(self.classified)
