from PyQt5 import QtCore, QtGui, QtWidgets

from utils import getSettings
from widgets.components.settingParametersWidgets import *


class SettingsWidget(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = getSettings()
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(7, 0, 7, 0)

        self.widgetLayout = QtWidgets.QVBoxLayout()
        self.widgetLayout.setContentsMargins(0, 0, 0, 20)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.topBar = QtWidgets.QGridLayout()

        self.layoutButton = QtWidgets.QHBoxLayout()

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))
        self.backButton.setToolTip("Back to home")
        self.backButton.clicked.connect(self.parent.navigateToHome)

        self.layoutButton.addWidget(self.backButton)
        self.topBar.addLayout(self.layoutButton, 0, 0)

        # Main label
        ## Make label
        self.mainLabel = QtWidgets.QLabel("Settings")
        self.mainLabel.setObjectName("settingsMainLabel")
        self.mainLabel.setAlignment(QtCore.Qt.AlignCenter)

        ## Add to top bar
        self.topBar.addWidget(self.mainLabel, 0, 1)
        
        # Empty label
        self.emptyLabel = QtWidgets.QLabel()
        self.topBar.addWidget(self.emptyLabel, 0, 2)
        
        # Add top bar to layout
        self.layout.addLayout(self.topBar)

        # Clustering parameters
        self.clusterWidget = ClusteringParametersWidget(self.settings)
        self.clusterWidget.showSettings()
        self.widgetLayout.addWidget(self.clusterWidget)

        # Pre processing parameters
        self.preProcessWidget = PreProcessingWidget(self.settings)
        self.widgetLayout.addWidget(self.preProcessWidget)

        # Segmentation parameters
        self.segmentationWidget = SegmentationWidget(self.settings)
        self.widgetLayout.addWidget(self.segmentationWidget)

        # Surface calculation
        self.surfaceWidget = SurfaceWidget(self.settings)
        self.widgetLayout.addWidget(self.surfaceWidget)

        # Calculations
        self.calculationsWidget = CalculationsWidget(self.settings)
        self.widgetLayout.addWidget(self.calculationsWidget)

        # Reset button
        self.resetButton = QtWidgets.QPushButton('Reset settings')
        self.resetButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.resetButton.setObjectName('buttonReset')
        self.resetButton.setMinimumHeight(30)
        self.resetButton.setContentsMargins(7, 0, 100, 0)
        self.resetButton.clicked.connect(self.resetSettingsValue)

        self.layout.addLayout(self.widgetLayout)
        self.layout.addWidget(self.resetButton)

        self.setLayout(self.layout)
    
    def resetSettingsValue(self):
        self.clusterWidget.resetValues()
        self.preProcessWidget.resetValues()
        self.segmentationWidget.resetValues()
        self.surfaceWidget.resetValues()
        self.calculationsWidget.resetValues()
