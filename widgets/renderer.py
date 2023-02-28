from PyQt5 import QtWidgets, QtCore, QtGui
import open3d as o3d
from widgets.components.resultTable import ResultTable
from widgets.components.resultTopBar import ResultTopBar
from widgets.components.buttonSpace import ButtonSpace
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import csv
from widgets.components.renderWidget import RenderWidget

class RendererWidget(QtWidgets.QWidget):
    def __init__(self, parent, fileName=None):
        super().__init__()
        self.fileName = fileName
        self.parent = parent
        self.acceptDrops = False
        self.classified = "data/results/result-classified.ply"
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)

        self.data = self.readData()
        
        self.renderWidget = RenderWidget(self.fileName, self)

        self.topBar = ResultTopBar(self.fileName, self.parent)
        self.buttonSpace = ButtonSpace(self)
        self.resultTable = ResultTable(self, self.data)

        total_area = sum([float(info["Surface area"]) for info in self.data])
        self.area_label = QtWidgets.QLabel(f"Total area: {total_area} m²")
        self.area_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.area_label.setAlignment(Qt.AlignCenter)
        self.area_label.setMaximumHeight(50)

        self.tableAndButtonSpace = QtWidgets.QWidget()
        self.tableAndButtonsLayout = QtWidgets.QVBoxLayout()

        self.tableAndButtonsLayout.addWidget(self.buttonSpace)
        self.tableAndButtonsLayout.addWidget(self.area_label)
        self.tableAndButtonsLayout.addWidget(self.resultTable)
        self.tableAndButtonSpace.setLayout(self.tableAndButtonsLayout)

        self.splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.renderWidget)
        self.splitter.addWidget(self.tableAndButtonSpace)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 5)
        self.splitter.setSizes([100,200])

        self.mergeBtn = QPushButton()
        self.mergeBtn.clicked.connect(lambda: self.resultTable.mergeSegments())
        self.mergeBtn.setText("Merge")

        layout.addWidget(self.topBar, 0, 0)
        layout.addWidget(self.splitter, 1, 0)
        layout.addWidget(self.mergeBtn, 2, 0)

        self.setLayout(layout)

        self.mergeBtn.hide()
    
    def changeGeometry(self, geometry):
        self.renderWidget.changeGeometry(geometry)
    
    def changeBackground(self):
        self.renderWidget.changeBackground()

    def readData(self):
        file = open("data/results/output.csv", "r")
        data = list(csv.DictReader(file, delimiter=","))
        file.close()
        return data
    
    def dataChanged(self):
        self.data = self.readData()
        total_area = sum([float(info["Surface area"]) for info in self.data])
        self.area_label.setText(f"Total area: {total_area} m²")
        self.resultTable.data = self.data
        self.resultTable.setData()

    def classifiedResultChanged(self):
        self.renderWidget.updateClassified()
    
    def clearSelectedPoints(self):
        self.renderWidget.clearSelectedPoints()
    
    def mergepoints(self):
        self.renderWidget.mergepoints()
    
    def getSelectedPoints(self):
        return self.renderWidget.getSelectedPoints()
    
    def getRenderedFile(self):
        return self.renderWidget.newFileName