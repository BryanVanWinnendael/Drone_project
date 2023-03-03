from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
import os
import zipfile

class ResultTopBar(QtWidgets.QWidget):
    def __init__(self, fileName, parent):
        super(ResultTopBar, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.parent = parent
        self.fileName = fileName

        self.layoutButton = QtWidgets.QHBoxLayout()
        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.clicked.connect(self.parent.navigateToHome)
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))
        self.backButton.setToolTip("Back to home")

        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setMaximumHeight(25)

        name = fileName.split("/")[-1].split(".")[0]
        self.nameLabel.setText(name)
        self.nameLabel.setObjectName("filelabel")
        
        self.layout.addWidget(self.backButton)
        self.layout.addWidget(self.nameLabel)

        self.saveButton = QtWidgets.QPushButton()
        self.saveButton.setIcon(QtGui.QIcon('assets/export.svg'))
        self.saveButton.setIconSize(QtCore.QSize(30, 30))
        self.saveButton.setObjectName("exportbtn")
        self.saveButton.setMinimumHeight(35)
        self.saveButton.setMaximumWidth(35)

        file = fileName.split("/")[-1]
        self.saveButton.setToolTip(f"Export {file} data")
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveButton.clicked.connect(self.saveDirectoryDialog)

        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)

    # Export the entire data directory to a zip file
    def saveDirectoryDialog(self):
        try:
            dirPath = QFileDialog.getExistingDirectory(self, "Select Directory")
            if dirPath == "":
                return
            resultPath = "data"
            zipPath = os.path.join(dirPath, "result.zip")
            print("Zipping directory:", zipPath)

            with zipfile.ZipFile(zipPath, "w", zipfile.ZIP_DEFLATED) as zip:
                for root, dirs, files in os.walk(resultPath):
                    for file in files:
                        absPath = os.path.join(root, file)
                        relPath = os.path.relpath(absPath, resultPath)
                        zip.write(absPath, relPath)

            print("Directory zipped and exported to:", zipPath)
        except:
            print("No directory selected")