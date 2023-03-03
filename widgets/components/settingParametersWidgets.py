from PyQt5 import QtCore, QtGui, QtWidgets
from utils import (clusterStrategies, surfaceStrategies, getSettings, resetSettings,
                   saveRecentFile, saveSettings)

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

class ClusteringParametersWidget(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.widget = QtWidgets.QWidget()
        self.setMaximumHeight(100)

        info_strategy = "Select the clustering strategy."
        self.strategyWidget = DropDown(clusterStrategies, "Cluster strategy", info_strategy, self.settings, callback=self.showSettings)

        info_epsilon = "The epsilon parameter is used in DBSCAN only. This parameter will be ignored with other strategies. It indicates the distances between clusters."
        self.epsilonWidget = TextInput(self.settings, 'Epsilon (DBSCAN)', info_epsilon)

        info_clusters = "The number of clusters to be used in Agglomerative clustering. This parameter will be ignored with other strategies. It indicates the number of clusters to be created. This number will be static so it will always create the same number of clusters per segment. This could be useful if you manually want to merge."
        self.clustersWidget = TextInput(self.settings, 'Number of Clusters (Agglomerative)', info_clusters)

        self.strategyWidget = DropDown(clusterStrategies, "Cluster strategy", info_strategy, self.settings, callback=self.showSettings)

        self.epsilonWidget = TextInput(self.settings, 'Epsilon (DBSCAN)', info_epsilon)

        self.clustersWidget = TextInput(self.settings, 'Number of Clusters (Agglomerative)', info_clusters)

        # self.layout = QtWidgets.QHBoxLayout()
        # self.layout.addWidget(self.strategyWidget)
        # self.layout.addWidget(self.epsilonWidget)
        # self.layout.addWidget(self.clustersWidget)
        # self.setLayout(self.layout)

        self.clusterVBox = QtWidgets.QVBoxLayout()

        self.clusterParameterLabel = QtWidgets.QLabel("Clustering parameters")
        self.clusterParameterLabel.setObjectName("settingsLabel")
        self.clusterVBox.addWidget(self.clusterParameterLabel)

        self.clusterParameterLayout = QtWidgets.QHBoxLayout()
        self.clusterParameterLayout.addWidget(self.strategyWidget)
        self.clusterParameterLayout.addWidget(self.epsilonWidget)
        self.clusterParameterLayout.addWidget(self.clustersWidget)

        self.clusterVBox.addLayout(self.clusterParameterLayout)

        self.setLayout(self.clusterVBox)

    def resetSettingsValue(self):
        defaultSettings = resetSettings()

        self.estimatedPlanesWidget.resetValue(defaultSettings)
        self.minimumPointsWidget.resetValue(defaultSettings)
        self.iterationsWidget.resetValue(defaultSettings)
        self.maxLoopsWidget.resetValue(defaultSettings)
        self.neighboursWidget.resetValue(defaultSettings)
        self.voxelSizeWidget.resetValue(defaultSettings)
        self.treshholdWidget.resetValue(defaultSettings)
        self.standardDeviationWidget.resetValue(defaultSettings)
        self.minRatioWidget.resetValue(defaultSettings)
        self.epsilonWidget.resetValue(defaultSettings)
        self.clustersWidget.resetValue(defaultSettings)

    def showSettings(self):
        cluster_strategy = self.strategyWidget.dropDown.currentText()

        if cluster_strategy == 'DBSCAN':
            self.clusterParameterLayout.addWidget(self.epsilonWidget)
            self.clusterParameterLayout.removeWidget(self.clustersWidget)
            self.clustersWidget.setParent(None)
        elif cluster_strategy == 'Agglomerative':
            self.clusterParameterLayout.addWidget(self.clustersWidget)
            self.clusterParameterLayout.removeWidget(self.epsilonWidget)
            self.epsilonWidget.setParent(None)
        else:
            self.clusterParameterLayout.removeWidget(self.epsilonWidget)
            self.epsilonWidget.setParent(None)
            self.clusterParameterLayout.removeWidget(self.clustersWidget)
            self.clustersWidget.setParent(None)