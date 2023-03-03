from PyQt5 import QtCore, QtGui, QtWidgets

from utils import (clusterStrategies, surfaceStrategies, getSettings, resetSettings,
                   saveRecentFile, saveSettings)
from widgets.components.settingParametersWidgets import *

class SettingsWidget(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = getSettings()
        
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()
        self.widget.setObjectName("widgetSettings")

        self.widgetLayout = QtWidgets.QVBoxLayout()
        self.widgetLayout.setSpacing(5)
        self.widgetLayout.setContentsMargins(0, 0, 0, 20)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.layoutButton = QtWidgets.QHBoxLayout()
        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.clicked.connect(self.parent.navigateToHome)
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))
        self.backButton.setToolTip("Back to home")
        self.layoutButton.addWidget(self.backButton)
        self.layout.addLayout(self.layoutButton)

        # Main label
        ## Make widget
        self.labelWidget = QtWidgets.QWidget()
        self.labelWidget.setObjectName("settingsLabelWidget")
        self.labelWidget.setMinimumHeight(70)
        self.labelWidget.setMaximumHeight(150)

        ## Make layout
        self.labelLayout = QtWidgets.QHBoxLayout()

        ## Make label
        self.mainLabel = QtWidgets.QLabel("Settings for the point cloud processing")
        self.mainLabel.setObjectName("settingsMainLabel")

        ## Add to layout
        self.labelLayout.addWidget(self.mainLabel)
        self.labelWidget.setLayout(self.labelLayout)
        self.layout.addWidget(self.labelWidget)

        # Clustering parameters
        self.clusterWidget = ClusteringParametersWidget(self.settings)
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
        self.resetButton.clicked.connect(self.resetSettingsValue)

        self.layout.addLayout(self.widgetLayout)
        self.layout.addWidget(self.resetButton)
        self.widget.setLayout(self.layout)

        self.setWidget(self.widget)
    
    def resetSettingsValue(self):
        defaultSettings = resetSettings()

        self.clusterWidget.resetValues(defaultSettings)
        self.preProcessWidget.resetValues(defaultSettings)
        self.segmentationWidget.resetValues(defaultSettings)
        self.surfaceWidget.resetValues(defaultSettings)
        self.calculationsWidget.resetValues(defaultSettings)
