from PyQt5 import QtWidgets, QtCore
from utils import getFileNames
from widgets.components.buttonHistory import ButtonHistory
from PyQt5.QtCore import pyqtSignal
from widgets.components.buttonUpload import ButtonUpload
from widgets.components.buttonSettings import ButtonSettings
from utils import checkDataDirectory, copyDirectory, cleanData
from widgets.components.buttonUploadPreProcessedData import ButtonUploadPreProcessedData
from widgets.components.toggle import AnimatedToggle

class HomeWidget(QtWidgets.QWidget):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self,parent):
        super(HomeWidget, self).__init__()
        self.parent = parent
        self.folderButton = False
        layout = QtWidgets.QVBoxLayout()
        self.setAcceptDrops(True)

        # Set error message label
        self.labelError = QtWidgets.QLabel()
        self.labelError.setMaximumHeight(25)
        self.labelError.setObjectName("label-error")
        layout.addWidget(self.labelError)

        topLayout = QtWidgets.QHBoxLayout()

        toggleLayout = QtWidgets.QHBoxLayout()
        mainToggle = AnimatedToggle()
        mainToggle.setCursor(QtCore.Qt.PointingHandCursor)
        mainToggle.setMaximumHeight(200)
        mainToggle.setMaximumWidth(60)
        mainToggle.clicked.connect(self.changeUploadButton)
        toggleLayout.addWidget(mainToggle)
        toggleText = QtWidgets.QLabel("Browse folder")
        toggleText.setMaximumHeight(40)
        toggleText.setMaximumWidth(90)
        toggleText.setObjectName("toggleText")
        toggleText.setAlignment(QtCore.Qt.AlignCenter)
        toggleLayout.addWidget(toggleText)

        topLayout.addLayout(toggleLayout)

        # Set settings button
        self.settingsButtonLayout = QtWidgets.QHBoxLayout()
        self.settingsButton = ButtonSettings(self.parent)
        self.settingsButtonLayout.addWidget(self.settingsButton)
        self.settingsButtonLayout.setAlignment(QtCore.Qt.AlignRight)
        topLayout.addLayout(self.settingsButtonLayout)

        layout.addLayout(topLayout)

        # Set upload buttons in horizontal layout
        uploadButtonsLayout = QtWidgets.QHBoxLayout()

        # Set upload button
        self.uploadButton = ButtonUpload(self)
        uploadButtonsLayout.addWidget(self.uploadButton)

        # Set upload pre processed data button
        self.uploadPreProcessedDataButton = ButtonUploadPreProcessedData(self)
        uploadButtonsLayout.addWidget(self.uploadPreProcessedDataButton)

        # Add upload buttons to layout
        layout.addLayout(uploadButtonsLayout)

        # Set recent files
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
        self.changeUploadButton()
    
    def changeUploadButton(self):
        self.folderButton = not self.folderButton
        self.uploadButton.setVisible(self.folderButton)
        self.uploadPreProcessedDataButton.setVisible(not self.folderButton)


    def openFileNameDialog(self):
        self.uploadButton.setNormal()
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file or directory", "", "Polygen Files (*).ply ", options=options)
        if fileName:
            if fileName.endswith('.ply'):
                self.parent.navigateToRenderer(fileName)
            else:
                self.uploadButton.setError()

    def openDirectoryDialog(self):
        self.uploadPreProcessedDataButton.setNormal()
        cleanData(True)
        options = QtWidgets.QFileDialog.Options()
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self, "Open file or directory", "", options=options)
        if fileName:
            if checkDataDirectory(fileName):
                copyDirectory(fileName, "data")
                self.parent.navigateToRendererFromPreProcessedData("data/results/original.ply")
            else:
                self.uploadPreProcessedDataButton.setError()

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
        elif checkDataDirectory(files[0]):
            cleanData(True)
            copyDirectory(files[0], "data")
            self.parent.navigateToRendererFromPreProcessedData("data/results/original.ply")
        else:
            print("Not a valid file")
            self.uploadButton.setError()
            self.uploadPreProcessedDataButton.setError()
