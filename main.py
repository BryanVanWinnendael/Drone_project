from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
import open3d as o3d
import numpy as np
import win32gui

# class PointCloudWidegt(QtWidgets.QWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.init_gui()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.init_gui()
  
    def init_gui(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        self.setCentralWidget(widget)
        ply_point_cloud = o3d.data.PLYPointCloud()
        pcd = o3d.io.read_point_cloud(ply_point_cloud.path)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(pcd)

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        self.window = QtGui.QWindow.fromWinId(hwnd)    
        self.windowcontainer = self.createWindowContainer(self.window, widget)
        layout.addWidget(self.windowcontainer, 0, 0)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_vis)
        timer.start(1)
    
    def update_vis(self):
        #self.vis.update_geometry()
        self.vis.poll_events()
        self.vis.update_renderer()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('o3d Embed')
    form.setGeometry(100, 100, 600, 500)
    form.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())