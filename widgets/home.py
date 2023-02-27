from PyQt5 import QtWidgets, QtCore
from utils import getFileNames
from widgets.components.buttonHistory import ButtonHistory
from PyQt5.QtCore import pyqtSignal
from widgets.components.buttonUpload import ButtonUpload
from widgets.components.buttonSettings import ButtonSettings

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
        self.settingsButton = ButtonSettings()
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