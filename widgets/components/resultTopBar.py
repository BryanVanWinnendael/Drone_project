from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

class ResultTopBar(QtWidgets.QWidget):
    def __init__(self, fileName, parent):
        super(ResultTopBar, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.parent = parent
        self.fileName = fileName

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.clicked.connect(self.parent.navigateToHome)
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))

        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setMaximumHeight(25)

        name = fileName.split("/")[-1].split(".")[0]
        self.nameLabel.setText(name)
        self.nameLabel.setObjectName("recentlabel")
        self.layout.addWidget(self.backButton)
        self.layout.addWidget(self.nameLabel)

        self.saveButton = QtWidgets.QPushButton("Export")
        self.saveButton.setObjectName("exportbtn")
        self.saveButton.setMinimumHeight(35)
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveButton.clicked.connect(self.saveFileDialog)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

    
    def saveFileDialog(self):
        try:
            filePath, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                            "CSV(*.csv);;")
            result_path = "data/results/output.csv"

            with open(result_path, "r") as infile:
                data = infile.read()

            with open(filePath, "w") as outfile:
                outfile.write(data)
        except:
            print("No file selected")