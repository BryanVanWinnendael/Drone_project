from PyQt5 import QtWidgets, QtGui, QtCore
from utils import getFileNames
from widgets.components.buttonHistory import ButtonHistory

class HomeWidget(QtWidgets.QWidget):
    def __init__(self,parent):
        super(HomeWidget, self).__init__()
        self.parent = parent
        layout = QtWidgets.QVBoxLayout()
        self.setAcceptDrops(True)

        self.label = QtWidgets.QLabel()
        self.label.setMaximumHeight(30)
        self.label.setObjectName("label-error")
        layout.addWidget(self.label)

        self.uploadButton = QtWidgets.QPushButton('Upload file')
        self.uploadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.uploadButton.setObjectName("uploadbtn")
        self.uploadButton.setIcon(QtGui.QIcon('assets/upload.svg'))
        self.uploadButton.setIconSize(QtCore.QSize(30, 30))
        self.uploadButton.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.uploadButton)

        vbox = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Recent files")
        label.setMaximumHeight(30)
        label.setObjectName("recentlabel")
        label.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(label)
        recentFiles = getFileNames()
        for file in recentFiles if recentFiles != None else []:
            btn = ButtonHistory(file, self.parent)
            vbox.addWidget(btn)
        layout.addLayout(vbox)

        self.setLayout(layout)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Polygon Files (*.ply)", options=options)
        if fileName and fileName.endswith('.ply'):
            self.parent.navigateToRenderer(fileName)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if (files[0].endswith('.ply') == True):
            print("Opening ply file")
            self.label.clear()
            self.parent.navigateToRenderer(files[0])
        else:
            self.label.setText("Not a ply file")
            print("Not a ply file")
    
    def renderIsLoading(self):
        self.label.setText("Loading...")
        self.uploadButton.setEnabled(False)