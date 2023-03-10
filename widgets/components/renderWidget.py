import win32gui
import numpy as np
import open3d as o3d

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
        self.newFileName = fileName
        self.widget = QtWidgets.QWidget()
        self.parent = parent
        self.classified = "data/results/result-classified.ply"
        self.night = False
        
        o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

        self.pcd = o3d.io.read_point_cloud(fileName)
        self.vis = o3d.visualization.VisualizerWithVertexSelection()
        self.vis.register_selection_changed_callback(self.onSelectionChanged)
        worker = WorkerCloseScreen(self)
        worker.start()

        self.vis.create_window()
        self.vis.add_geometry(self.pcd)
        self.vis.run()

        win32gui.CloseWindow(win32gui.FindWindowEx(0, 0, None, "Open3D - free view"))
        
        self.classified_pcd = o3d.io.read_point_cloud(self.classified)

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D - free view")
        self.window = QtGui.QWindow.fromWinId(hwnd)    

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.windowcontainer = self.parent.createWindowContainer(self.window, self.widget)
        self.windowcontainer.setMinimumWidth(300)
        self.windowcontainer.setMinimumHeight(300)
        self.vbox.addWidget(self.windowcontainer)

        self.timer = QtCore.QTimer(self.parent)
        self.timer.timeout.connect(self.updateVis)
        self.timer.start(1)

        self.setLayout(self.vbox)

    def updateVis(self):
        self.vis.poll_events()
        self.vis.update_renderer()
    
    def changeGeometry(self, newFileName):
        original_view = self.vis.get_view_control().convert_to_pinhole_camera_parameters() 
        self.newFileName = newFileName
       
        self.clearSelectedPoints()
        self.vis.clear_geometries()

        if newFileName == self.fileName:
            self.vis.add_geometry(self.pcd)

        elif newFileName == self.classified:
            self.vis.add_geometry(self.classified_pcd)
        else:
            cloud = o3d.io.read_point_cloud(newFileName)
            try:
                self.vis.add_geometry(cloud)
            except RuntimeError as error:
                print("Error: Could not load file")
                print(error)
                self.changeGeometry(self.classified)
            except:
                print("Other error")

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

    def updateRenderClassified(self):
        self.classified_pcd = o3d.io.read_point_cloud(self.classified)
        self.changeGeometry(self.classified)

    def updateClassified(self):
        self.classified_pcd = o3d.io.read_point_cloud(self.classified)
    
    def clearSelectedPoints(self):
        self.vis.clear_picked_points()
    
    def getSelectedPoints(self):
        return self.vis.get_picked_points()

    def onSelectionChanged(self):
        if self.newFileName == self.fileName or self.newFileName == self.classified:
            self.clearSelectedPoints()
        else:
            if len(self.getSelectedPoints()) > 0:
                self.parent.deleteButton.setEnabled(True)
                self.parent.deleteButton.show()
            else:
                self.parent.deleteButton.setEnabled(False)
                self.parent.deleteButton.hide()