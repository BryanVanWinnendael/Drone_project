from PyQt5 import QtCore, QtWidgets, QtGui
import open3d as o3d
import win32gui

class PointCloud_MainWindow(QtWidgets.QWidget):
    backSignal = QtCore.pyqtSignal()
    def __init__(self, fileName=None):
        super().__init__()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)

        print(fileName)

        pcd = o3d.io.read_point_cloud(fileName)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(pcd)

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")

        self.window = QtGui.QWindow.fromWinId(hwnd)    
        self.windowcontainer = self.createWindowContainer(self.window, widget)

        button = QtWidgets.QPushButton('Upload new file')
        button.clicked.connect(self.goBack)
        layout.addWidget(button, 0, 0)
        layout.addWidget(self.windowcontainer, 1, 0)

        self.setLayout(layout)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_vis)
        timer.start(1)

    def update_vis(self):
        self.vis.poll_events()
        self.vis.update_renderer()
    
    def goBack(self):
        # self.close()
        self.backSignal.emit()