from PyQt5 import QtCore, QtGui, QtWidgets

from utils import (clusterStrategies, surfaceStrategies, getSettings, resetSettings,
                   saveRecentFile, saveSettings)
from widgets.components.settingParametersWidgets import *


class DropDown(QtWidgets.QWidget):
    def __init__(self, items, value, info, settings, callback=None):
        super(DropDown, self).__init__()
        self.items = items
        self.value = value
        self.info = info
        self.settings = settings
        self.callback = callback

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layoutText = QtWidgets.QHBoxLayout()
        self.layoutText.setContentsMargins(0, 0, 0, 5)
        self.layoutText.setSpacing(10)

        self.textLabel = QtWidgets.QLabel(self.value)
        self.textLabel.setObjectName('infoLabel')
        self.buttonInfo = QtWidgets.QPushButton()
        self.buttonInfo.setIcon(QtGui.QIcon('assets/info.svg'))
        self.buttonInfo.setIconSize(QtCore.QSize(20, 20))
        self.buttonInfo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonInfo.setObjectName('buttonInfo')
        self.buttonInfo.setToolTip(self.info)
        self.buttonInfo.clicked.connect(lambda: QtWidgets.QMessageBox.information(self, 'Info', self.info))

        self.layoutText.addWidget(self.textLabel)
        self.layoutText.addWidget(self.buttonInfo)

        self.dropDown = QtWidgets.QComboBox()
        for item in self.items:
            self.dropDown.addItem(item)
        
        self.dropDown.setCurrentText(self.settings[self.value])

        self.dropDown.currentIndexChanged.connect(self.saveSettingsValue)

        self.layout.addLayout(self.layoutText)
        self.layout.addWidget(self.dropDown)

        self.setLayout(self.layout)

    def saveSettingsValue(self):
        if self.callback: self.callback()
        self.settings[self.value] = self.dropDown.currentText()
        saveSettings(self.settings)
        saveRecentFile(None)

class TextInput(QtWidgets.QWidget):
    def __init__(self, settings, value, info, steps=0.5):
        super(TextInput, self).__init__()
        self.settings = settings
        self.value = value
        self.info = info

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)

        self.layoutText = QtWidgets.QHBoxLayout()
        self.layoutText.setContentsMargins(0, 0, 0, 5)

        self.textLabel = QtWidgets.QLabel(self.value)
        self.textLabel.setObjectName('infoLabel')
        self.buttonInfo = QtWidgets.QPushButton()
        self.buttonInfo.setIcon(QtGui.QIcon('assets/info.svg'))
        self.buttonInfo.setIconSize(QtCore.QSize(20, 20))
        self.buttonInfo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonInfo.setObjectName('buttonInfo')
        self.buttonInfo.setToolTip(self.info)
        self.buttonInfo.clicked.connect(lambda: QtWidgets.QMessageBox.information(self, 'Info', self.info))

        self.layoutText.addWidget(self.textLabel)
        self.layoutText.addWidget(self.buttonInfo)

        self.TextWidget = QtWidgets.QDoubleSpinBox()
        self.TextWidget.setSingleStep(steps)
        self.TextWidget.setRange(0, 100000)
        self.TextWidget.setValue(self.settings[self.value])
        self.TextWidget.valueChanged.connect(self.saveSettingsValue)

        self.layout.addLayout(self.layoutText)
        self.layout.addWidget(self.TextWidget)

        self.setLayout(self.layout)

    def saveSettingsValue(self):
        self.settings[self.value] = self.TextWidget.value()
        saveSettings(self.settings)
        saveRecentFile(None)
    
    def resetValue(self, defaultSettings):
        self.TextWidget.setValue(defaultSettings[self.value])
        saveRecentFile(None)

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
        # self.widgetLayout.setAlignment(QtCore.Qt.AlignCenter)
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

        self.mainLabel = QtWidgets.QLabel("Settings for the point cloud processing")
        self.mainLabel.setObjectName("settingsMainLabel")
        self.widgetLayout.addWidget(self.mainLabel)

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

        # self.showSettings()
        self.setWidget(self.widget)
    
    def resetSettingsValue(self):
        defaultSettings = resetSettings()

        self.clusterWidget.resetValues(defaultSettings)
        self.preProcessWidget.resetValues(defaultSettings)
        self.segmentationWidget.resetValues(defaultSettings)
        self.surfaceWidget.resetValues(defaultSettings)
        self.calculationsWidget.resetValues(defaultSettings)
