from PyQt5 import QtCore, QtGui, QtWidgets

from utils import (clusterStrategies, getSettings, resetSettings,
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
        self.callback()
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

        self.widgetLayout = QtWidgets.QVBoxLayout(self)
        self.widgetLayout.setSpacing(20)

        self.layoutButton = QtWidgets.QHBoxLayout()
        self.layoutButton.setContentsMargins(-10, 0, 0, 10)
        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.setObjectName("backbtn")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.clicked.connect(self.parent.navigateToHome)
        self.backButton.setIcon(QtGui.QIcon('assets/back.svg'))
        self.backButton.setIconSize(QtCore.QSize(30, 30))
        self.backButton.setToolTip("Back to home")
        self.layoutButton.addWidget(self.backButton)

        info_strategy = "Select the clustering strategy."
        self.strategyWidget = DropDown(clusterStrategies, "Cluster strategy", info_strategy, self.settings, callback=self.showSettings)

        info_minimumPoints = "This is the minimum number of points that a segment/ cluster needs to have."
        self.minimumPointsWidget = TextInput(self.settings, 'Minimum points', info_minimumPoints)

        info_iterations = "The number of iterations to run the RANSAC algorithm for."
        self.iterationsWidget = TextInput(self.settings, 'Iterations', info_iterations)

        info_maxLoops = "The maximum number of loops to run the RANSAC algorithm for, this is to prevent infinite loops or if you manually want to limit the amount of segments."
        self.maxLoopsWidget = TextInput(self.settings, 'Maximum number of loops', info_maxLoops)

        neighbourhbours = "The number of neighbours that are used to remove outliers."
        self.neighboursWidget = TextInput(self.settings, 'Number of neighbours', neighbourhbours)

        info_voxelSize = "The size of the voxel for downsampling the point cloud. The smaller the voxel size, the more points will be removed."
        self.voxelSizeWidget = TextInput(self.settings, 'Voxel size', info_voxelSize)

        info_treshhold = "The treshold for the RANSAC algorithm. The smaller the treshold, the more points will be removed."
        self.treshholdWidget = TextInput(self.settings, 'Treshold', info_treshhold, 0.01)

        info_standardDeviation = "The standard deviation ratio to remove statistical outliers."
        self.standardDeviationWidget = TextInput(self.settings, 'Standard deviation ratio', info_standardDeviation)

        info_minRatio = "The ratio parameter determines when the segmenting stops, segmenting will stop if the ratio of points is reached. For example if the ratio is 0.1, the segmenting will stop when 10% of the points are left."
        self.minRatioWidget = TextInput(self.settings, 'Minimum ratio', info_minRatio, 0.01)

        info_epsilon = "The epsilon parameter is used in DBSCAN only. This parameter will be ignored with other strategies. It indicates the distances between clusters."
        self.epsilonWidget = TextInput(self.settings, 'Epsilon (DBSCAN)', info_epsilon)

        info_clusters = "The number of clusters to be used in Agglomerative clustering. This parameter will be ignored with other strategies. It indicates the number of clusters to be created. This number will be static so it will always create the same number of clusters per segment. This could be useful if you manually want to merge."
        self.clustersWidget = TextInput(self.settings, 'Number of Clusters (Agglomerative)', info_clusters)
        
        self.widgetLayout.addLayout(self.layoutButton)
        self.widgetLayout.addWidget(self.strategyWidget)
        self.widgetLayout.addWidget(self.minimumPointsWidget)
        self.widgetLayout.addWidget(self.iterationsWidget)
        self.widgetLayout.addWidget(self.maxLoopsWidget)
        self.widgetLayout.addWidget(self.neighboursWidget)
        self.widgetLayout.addWidget(self.voxelSizeWidget)
        self.widgetLayout.addWidget(self.treshholdWidget)
        self.widgetLayout.addWidget(self.standardDeviationWidget)
        self.widgetLayout.addWidget(self.minRatioWidget)

        resetButton = QtWidgets.QPushButton('Reset')
        resetButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        resetButton.setObjectName('buttonReset')
        resetButton.setMinimumHeight(30)
        resetButton.clicked.connect(self.resetSettingsValue)

        self.showSettings()

        self.setLayout(self.widgetLayout)
    
    def resetSettingsValue(self):
        defaultSettings = resetSettings()

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
            self.widgetLayout.addWidget(self.epsilonWidget)
            self.widgetLayout.removeWidget(self.clustersWidget)
            self.clustersWidget.setParent(None)
        elif cluster_strategy == 'Agglomerative':
            self.widgetLayout.addWidget(self.clustersWidget)
            self.widgetLayout.removeWidget(self.epsilonWidget)
            self.epsilonWidget.setParent(None)
        else:
            self.widgetLayout.removeWidget(self.epsilonWidget)
            self.epsilonWidget.setParent(None)
            self.widgetLayout.removeWidget(self.clustersWidget)
            self.clustersWidget.setParent(None)

            
        
        

    


        
    