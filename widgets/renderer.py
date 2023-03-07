import csv
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from model.removePoints import removePoints
from utils import getSettings
from widgets.components.buttonSpace import ButtonSpace
from widgets.components.renderWidget import RenderWidget
from widgets.components.resultTable import ResultTable
from widgets.components.resultTopBar import ResultTopBar


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
        self.area_label.setObjectName("info_label")
        self.area_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.area_label.setAlignment(Qt.AlignCenter)
        self.area_label.setMaximumHeight(50)

        self.settings = getSettings()
        estimated_planes = self.settings["Estimated planes"]
        if estimated_planes == 0:
            self.correctness_label = QtWidgets.QLabel(f"No estimated planes provided")
        if estimated_planes > 0:
            self.correctness_label = QtWidgets.QLabel(f"Segmentation correctness: {self.calculateCorrectness(estimated_planes)}%")
        
        self.correctness_label.setObjectName("info_label")

        self.correctness_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.correctness_label.setAlignment(Qt.AlignCenter)
        self.correctness_label.setMaximumHeight(50)

        self.tableAndButtonSpace = QtWidgets.QWidget()
        self.rendererLayout = QtWidgets.QVBoxLayout()

        # Make seperate horizontal layout for the info labels
        self.infoLayout = QtWidgets.QHBoxLayout()
        self.infoLayout.addWidget(self.area_label)
        self.infoLayout.addWidget(self.correctness_label)

        # Make layout for the table and buttons
        self.tableAndButtonsLayout = QtWidgets.QVBoxLayout()
        self.tableAndButtonsLayout.addWidget(self.buttonSpace)
        self.tableAndButtonsLayout.addLayout(self.infoLayout)
        self.tableAndButtonsLayout.addWidget(self.resultTable)
        self.tableAndButtonsLayout.setSpacing(0)
        self.tableAndButtonsLayout.setContentsMargins(0, 0, 0, 0)

        # self.rendererLayout.addLayout(self.infoLayout)
        self.rendererLayout.addLayout(self.tableAndButtonsLayout)

        self.tableAndButtonSpace.setLayout(self.rendererLayout)
        self.rendererLayout.setSpacing(0)
        self.rendererLayout.setContentsMargins(0, 0, 0, 0)
        
        self.splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.renderWidget)
        self.splitter.addWidget(self.tableAndButtonSpace)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 5)
        self.splitter.setSizes([100,200])

        self.mergeBtn = QPushButton()
        self.mergeBtn.setObjectName("mergeBtn")
        self.mergeBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.mergeBtn.clicked.connect(lambda: self.resultTable.mergeSegments())
        self.mergeBtn.setText("Merge")

        self.deleteButton = QPushButton()
        self.deleteButton.setObjectName("deleteBtn")
        self.deleteButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteButton.clicked.connect(lambda: self.removeSelectedPoints())
        self.deleteButton.setText("Delete selection")

        layout.addWidget(self.topBar, 0, 0)
        layout.addWidget(self.splitter, 1, 0)
        layout.addWidget(self.mergeBtn, 2, 0)
        layout.addWidget(self.deleteButton, 3, 0)

        self.setLayout(layout)

        self.mergeBtn.hide()
        self.deleteButton.hide()
    
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
        if self.settings["Estimated planes"] > 0:
            estimated_planes = self.settings["Estimated planes"]
            self.correctness_label.setText(f"Segmentation correctness: {self.calculateCorrectness(estimated_planes)}%")
        self.resultTable.clearChecks()
        self.resultTable.data = self.data
        self.resultTable.setData()

        # Hide buttons
        self.mergeBtn.hide()
        self.deleteButton.hide()

    def classifiedResultChanged(self):
        self.renderWidget.updateRenderClassified()
    
    def clearSelectedPoints(self):
        self.renderWidget.clearSelectedPoints()
    
    def mergepoints(self):
        self.renderWidget.mergepoints()
    
    def getSelectedPoints(self):
        return self.renderWidget.getSelectedPoints()
    
    def getRenderedFile(self):
        return self.renderWidget.newFileName
    
    def calculateCorrectness(self, estimated_planes):
        if len(self.data) > estimated_planes:
            return estimated_planes / len(self.data) * 100
        else:
            return len(self.data) / int(estimated_planes) * 100
        
    def removeSelectedPoints(self):
        removePoints(self.renderWidget.newFileName, self.getSelectedPoints(), self.resultTable.checkedButtons)
        self.clearSelectedPoints()
        self.deleteButton.hide()
        self.deleteButton.setEnabled(False)
        self.renderWidget.updateVis()
        self.renderWidget.updateClassified()
        if not os.path.exists(self.renderWidget.newFileName):
            self.changeGeometry(self.renderWidget.classified)
        else:
            self.changeGeometry(self.renderWidget.newFileName)

        self.dataChanged()
        self.resultTable.clearChecks()