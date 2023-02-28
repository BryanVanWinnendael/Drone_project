from PyQt5 import QtCore, QtGui, QtWidgets

from utils import (clusterStrategies, getSettings, resetSettings,
                   saveRecentFile, saveSettings)


class DropDown(QtWidgets.QWidget):
    def __init__(self, items, value, info, settings):
        super(DropDown, self).__init__()
        self.items = items
        self.value = value
        self.info = info
        self.settings = settings

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layoutText = QtWidgets.QHBoxLayout()
        self.layoutText.setContentsMargins(0, 0, 0, 10)
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
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layoutText = QtWidgets.QHBoxLayout()
        self.layoutText.setContentsMargins(0, 0, 0, 10)
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

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = getSettings()

        widgetLayout = QtWidgets.QVBoxLayout(self)
        widgetLayout.setSpacing(20)

        self.layoutButton = QtWidgets.QHBoxLayout()
        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.clicked.connect(self.parent.navigateToHome)
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))
        self.backButton.setToolTip("Back to home")

        info_strategy = ""
        self.strategyWidget = DropDown(clusterStrategies, "Cluster strategy", info_strategy, self.settings)

        info_minimumPoints = ""
        self.minimumPointsWidget = TextInput(self.settings, 'Minimum points', info_minimumPoints)

        info_iterations = ""
        self.iterationsWidget = TextInput(self.settings, 'Iterations', info_iterations)

        info_maxLoops = ""
        self.maxLoopsWidget = TextInput(self.settings, 'Maximum number of loops', info_maxLoops)

        info_neigbours = ""
        self.neigboursWidget = TextInput(self.settings, 'Number of neigbours', info_neigbours)

        info_voxelSize = ""
        self.voxelSizeWidget = TextInput(self.settings, 'Voxel size', info_voxelSize)

        info_treshhold = ""
        self.treshholdWidget = TextInput(self.settings, 'Treshold', info_treshhold, 0.01)

        info_standardDeviation = ""
        self.standardDeviationWidget = TextInput(self.settings, 'Standard deviation ratio', info_standardDeviation)

        info_minRatio = ""
        self.minRatioWidget = TextInput(self.settings, 'Minimum ratio', info_minRatio, 0.01)

        widgetLayout.addWidget(self.backButton)
        widgetLayout.addWidget(self.strategyWidget)
        widgetLayout.addWidget(self.minimumPointsWidget)
        widgetLayout.addWidget(self.iterationsWidget)
        widgetLayout.addWidget(self.maxLoopsWidget)
        widgetLayout.addWidget(self.neigboursWidget)
        widgetLayout.addWidget(self.voxelSizeWidget)
        widgetLayout.addWidget(self.treshholdWidget)
        widgetLayout.addWidget(self.standardDeviationWidget)
        widgetLayout.addWidget(self.minRatioWidget)

        resetButton = QtWidgets.QPushButton('Reset')
        resetButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        resetButton.setObjectName('buttonReset')
        resetButton.setMinimumHeight(30)
        resetButton.clicked.connect(self.resetSettingsValue)

        self.setLayout(widgetLayout)
    
    def resetSettingsValue(self):
        defaultSettings = resetSettings()

        self.minimumPointsWidget.resetValue(defaultSettings)
        self.iterationsWidget.resetValue(defaultSettings)
        self.maxLoopsWidget.resetValue(defaultSettings)
        self.neigboursWidget.resetValue(defaultSettings)
        self.voxelSizeWidget.resetValue(defaultSettings)
        self.treshholdWidget.resetValue(defaultSettings)
        self.standardDeviationWidget.resetValue(defaultSettings)
        self.minRatioWidget.resetValue(defaultSettings)


        
    