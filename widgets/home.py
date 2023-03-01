from PyQt5 import QtWidgets, QtCore
from utils import getFileNames
from widgets.components.buttonHistory import ButtonHistory
from PyQt5.QtCore import pyqtSignal
from widgets.components.buttonUpload import ButtonUpload
from widgets.components.buttonSettings import ButtonSettings
from widgets.components.buttonUploadPreProcessedData import ButtonUploadPreProcessedData
import os
from utils import copyDirectory

class HomeWidget(QtWidgets.QWidget):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self,parent):
        super(HomeWidget, self).__init__()
        self.parent = parent
        layout = QtWidgets.QVBoxLayout()
        self.setAcceptDrops(True)

        self.labelError = QtWidgets.QLabel()
        self.labelError.setMaximumHeight(25)
        self.labelError.setObjectName("label-error")
        layout.addWidget(self.labelError)

        self.settingsButtonLayout = QtWidgets.QHBoxLayout()
        self.settingsButton = ButtonSettings(self.parent)
        self.settingsButtonLayout.addWidget(self.settingsButton)
        self.settingsButtonLayout.setAlignment(QtCore.Qt.AlignRight)
        layout.addLayout(self.settingsButtonLayout)

        widget = QtWidgets.QWidget()
        self.uploadButtonLayout = QtWidgets.QGridLayout(widget)
        self.textLayout = QtWidgets.QHBoxLayout()

        self.uploadText = QtWidgets.QLabel("Drag file here or")
        self.uploadText.setObjectName("uploadtext")
        self.textLayout.addWidget(self.uploadText)

        self.uploadText2 = QtWidgets.QLabel("browse")
        self.uploadText2.setObjectName("uploadtext2")
        self.textLayout.addWidget(self.uploadText2)

        self.uploadButton = ButtonUpload(self)
        layout.addWidget(self.uploadButton)

        self.uploadPreProcessedDataButton = ButtonUploadPreProcessedData(self)
        layout.addWidget(self.uploadPreProcessedDataButton)

        vbox = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel("Recent files")
        self.label.setMaximumHeight(40)
        self.label.setObjectName("recentlabel")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        vbox.addWidget(self.label)
        recentFiles = getFileNames()
        for file in recentFiles if recentFiles != None else []:
            btn = ButtonHistory(file, self.parent)
            vbox.addWidget(btn)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        layout.addLayout(vbox)

        self.setLayout(layout)

    def openFileNameDialog(self):
        self.uploadButton.setNormal()
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open point cloud file", "","Polygon Files (*.ply)", options=options)
        if fileName and fileName.endswith('.ply'):
            self.parent.navigateToRenderer(fileName)

    def openDirectoryDialog(self):
        self.uploadButton.setNormal()
        options = QtWidgets.QFileDialog.Options()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,"Open exported data file", "", options=options)
        if directory:
            contents = os.listdir(directory)
            
            # Check if the correct folders exist
            if "planes" not in contents or "results" not in contents:
                self.uploadPreProcessedDataButton.setError()
                return
            
            # Check if the results folder contains the correct files
            results = os.listdir(os.path.join(directory, "results"))
            if "original.ply" not in results or "result-classified.ply" not in results or "output.csv" not in results:
                self.uploadPreProcessedDataButton.setError()
                return
            
            # Copy the files to the data folder
            copyDirectory(directory, "data")

            # Navigate to the renderer
            self.parent.navigateToRendererFromPreProcessedData(os.path.join("data", "results", "original.ply"))
            
    
    def dragEnterEvent(self, event):
        self.uploadButton.setNormal()
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if (files[0].endswith('.ply') == True):
            print("Opening ply file")
            self.parent.navigateToRenderer(files[0])
        else:
            print("Not a ply file")
            self.uploadButton.setError()