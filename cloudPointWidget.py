from PyQt5 import QtWidgets
import open3d as o3d
from PyQt5 import QtCore
from PyQt5 import QtGui
import win32gui

class CloudPointWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()
        
    def init_gui(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)

        ply_point_cloud = o3d.data.PLYPointCloud()
        pcd = o3d.io.read_point_cloud(ply_point_cloud.path)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(pcd)

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        self.window = QtGui.QWindow.fromWinId(hwnd)    
        self.windowcontainer = self.createWindowContainer(self.window, widget)
        layout.addWidget(self.windowcontainer, 0, 0)
        self.setLayout(layout)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_vis)
        timer.start(1)

    def update_vis(self):
        self.vis.poll_events()
        self.vis.update_renderer()