from PyQt5 import QtCore, QtGui, QtWidgets
from utils import (clusterStrategies, surfaceStrategies, resetSettings,
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
    
    def resetValue(self, defaultSettings):
        self.dropDown.setCurrentText(defaultSettings[self.value])

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

class Switch(QtWidgets.QWidget):
    def __init__(self, settings, value, info):
        super(Switch, self).__init__()
        self.settings = settings
        self.value = value
        self.info = info

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.setMaximumWidth(300)

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

        self.CheckBox = QtWidgets.QCheckBox()
        self.CheckBox.setMinimumHeight(35)
        self.CheckBox.setChecked(self.settings[self.value])
        self.CheckBox.toggled.connect(self.saveSettingsValue)

        self.layout.addLayout(self.layoutText)
        self.layout.addWidget(self.CheckBox)

        self.setLayout(self.layout)

    def saveSettingsValue(self, state):
        self.settings[self.value] = state
        saveSettings(self.settings)
        saveRecentFile(None)
    
    def resetValue(self, defaultSettings):
        self.CheckBox.setChecked(defaultSettings[self.value])
        saveRecentFile(None)

class ClusteringParametersWidget(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.widget = QtWidgets.QWidget()
        self.setMaximumHeight(130)

        # Clustering parameters
        info_strategy = "Select the clustering strategy."
        self.strategyWidget = DropDown(clusterStrategies, "Cluster strategy", info_strategy, self.settings, callback=self.showSettings)

        info_redistribute = "This option selects wether or not you want to redistribute smaller clusters back into the segmentation process.\nSelecting this will search for the largest cluster and only use that as a segment. The remaining cluster points will be put back into the segmentation cycle so that they can be segmentated with other points.\nUnselecting this will result in all the clusters that were detected by the strategy being identified as seperate segments."
        self.redistributeWidget = Switch(self.settings, 'Redistribute smaller clusters', info_redistribute)

        info_epsilon = "The epsilon parameter is used in DBSCAN only. This parameter will be ignored with other strategies.\nIt indicates the distances between clusters."
        self.epsilonWidget = TextInput(self.settings, 'Epsilon (DBSCAN)', info_epsilon)

        info_clusters = "The number of clusters to be used in Agglomerative clustering. This parameter will be ignored with other strategies.\n\nIt indicates the number of clusters to be created.\nThis number will be static so it will always create the same number of clusters per segment. This could be useful if you manually want to merge."
        self.clustersWidget = TextInput(self.settings, 'Number of Clusters (Agglomerative)', info_clusters, steps=1)

        self.box = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Clustering parameters")
        self.label.setObjectName("settingsLabel")
        self.label.setContentsMargins(7, 0, 0, 0)
        self.box.addWidget(self.label)

        self.parameterLayout = QtWidgets.QHBoxLayout()
        self.parameterLayout.addWidget(self.strategyWidget)
        self.parameterLayout.addWidget(self.redistributeWidget)

        self.box.addLayout(self.parameterLayout)
        self.setLayout(self.box)

    def showSettings(self):
        cluster_strategy = self.strategyWidget.dropDown.currentText()

        if cluster_strategy == 'DBSCAN':
            self.parameterLayout.addWidget(self.epsilonWidget)
            self.parameterLayout.removeWidget(self.clustersWidget)
            self.clustersWidget.setParent(None)
        elif cluster_strategy == 'Agglomerative':
            self.parameterLayout.addWidget(self.clustersWidget)
            self.parameterLayout.removeWidget(self.epsilonWidget)
            self.epsilonWidget.setParent(None)
        else:
            self.parameterLayout.removeWidget(self.epsilonWidget)
            self.epsilonWidget.setParent(None)
            self.parameterLayout.removeWidget(self.clustersWidget)
            self.clustersWidget.setParent(None)

    def resetValues(self):
        defaultSettings = resetSettings()

        self.strategyWidget.resetValue(defaultSettings)
        self.epsilonWidget.resetValue(defaultSettings)
        self.clustersWidget.resetValue(defaultSettings)

class PreProcessingWidget(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.widget = QtWidgets.QWidget()
        self.setMaximumHeight(130)
    
        # Make Widgets
        neighbourhbours = "The number of neighbours that are used to remove outliers."
        self.neighboursWidget = TextInput(self.settings, 'Number of neighbours', neighbourhbours, steps=1)

        info_voxelSize = "The size of the voxel for downsampling the point cloud. The smaller the voxel size, the more points will be removed."
        self.voxelSizeWidget = TextInput(self.settings, 'Voxel size', info_voxelSize)

        info_standardDeviation = "The standard deviation ratio to remove statistical outliers."
        self.standardDeviationWidget = TextInput(self.settings, 'Standard deviation ratio', info_standardDeviation)

        # Make Layout
        self.box = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Pre processing parameters")
        self.label.setObjectName("settingsLabel")
        self.label.setContentsMargins(7, 0, 0, 0)
        self.box.addWidget(self.label)

        self.parameterLayout = QtWidgets.QHBoxLayout()
        self.parameterLayout.addWidget(self.neighboursWidget)
        self.parameterLayout.addWidget(self.voxelSizeWidget)
        self.parameterLayout.addWidget(self.standardDeviationWidget)

        self.box.addLayout(self.parameterLayout)

        self.setLayout(self.box)

    def resetValues(self):
        defaultSettings = resetSettings()

        self.neighboursWidget.resetValue(defaultSettings)
        self.voxelSizeWidget.resetValue(defaultSettings)
        self.standardDeviationWidget.resetValue(defaultSettings)

class SegmentationWidget(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.widget = QtWidgets.QWidget()
        self.setMaximumHeight(130)
    
        # Make Widgets
        info_minimumPoints = "This is the minimum number of points that a segment/ cluster needs to have."
        self.minimumPointsWidget = TextInput(self.settings, 'Minimum points', info_minimumPoints, steps=1)

        info_iterations = "The number of iterations to run the RANSAC algorithm for."
        self.iterationsWidget = TextInput(self.settings, 'Iterations', info_iterations, steps=1)

        info_maxLoops = "The maximum number of loops to run the RANSAC algorithm for, this is to prevent infinite loops or if you manually want to limit the amount of segments."
        self.maxLoopsWidget = TextInput(self.settings, 'Maximum number of loops', info_maxLoops)

        info_treshhold = "The treshold for the RANSAC algorithm. The smaller the treshold, the more points will be removed."
        self.treshholdWidget = TextInput(self.settings, 'Treshold', info_treshhold, 0.01)

        info_minRatio = "The ratio parameter determines when the segmenting stops, segmenting will stop if the ratio of points is reached.\n\nFor example if the ratio is 0.1, the segmenting will stop when 10% of the points are left."
        self.minRatioWidget = TextInput(self.settings, 'Minimum ratio', info_minRatio, 0.01)

        # Make Layout
        self.box = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Segmentation parameters")
        self.label.setObjectName("settingsLabel")
        self.label.setContentsMargins(7, 0, 0, 0)
        self.box.addWidget(self.label)

        self.parameterLayout = QtWidgets.QHBoxLayout()
        self.parameterLayout.addWidget(self.minimumPointsWidget)
        self.parameterLayout.addWidget(self.iterationsWidget)
        self.parameterLayout.addWidget(self.maxLoopsWidget)
        self.parameterLayout.addWidget(self.treshholdWidget)
        self.parameterLayout.addWidget(self.minRatioWidget)

        self.box.addLayout(self.parameterLayout)

        self.setLayout(self.box)

    def resetValues(self):
        defaultSettings = resetSettings()

        self.minimumPointsWidget.resetValue(defaultSettings)
        self.iterationsWidget.resetValue(defaultSettings)
        self.maxLoopsWidget.resetValue(defaultSettings)
        self.treshholdWidget.resetValue(defaultSettings)
        self.minRatioWidget.resetValue(defaultSettings)

class SurfaceWidget(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.widget = QtWidgets.QWidget()
        self.setMaximumHeight(130)

        # Make Widgets
        info_surfaceStrategy = "Select the surface calculation strategy."
        self.surfaceStrategyWidget = DropDown(surfaceStrategies, "Surface strategy", info_surfaceStrategy, self.settings)

        # Make Layout
        self.box = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Surface parameters")
        self.label.setObjectName("settingsLabel")
        self.label.setContentsMargins(7, 0, 0, 0)
        self.box.addWidget(self.label)

        self.parameterLayout = QtWidgets.QHBoxLayout()
        self.parameterLayout.addWidget(self.surfaceStrategyWidget)

        self.box.addLayout(self.parameterLayout)

        self.setLayout(self.box)

    def resetValues(self):
        defaultSettings = resetSettings()

        self.surfaceStrategyWidget.resetValue(defaultSettings)

class CalculationsWidget(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.widget = QtWidgets.QWidget()
        self.setMaximumHeight(130)

        # Make Widgets
        info_estimatedPlanes = "The number of planes you think will be in the point cloud. This is used to calculate the correctness of the segmentation."
        self.estimatedPlanesWidget = TextInput(self.settings, 'Estimated planes', info_estimatedPlanes, steps=1)

        # Make Layout
        self.box = QtWidgets.QVBoxLayout()

        self.box = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Calculations parameters")
        self.label.setObjectName("settingsLabel")
        self.label.setContentsMargins(7, 0, 0, 0)
        self.box.addWidget(self.label)

        self.parameterLayout = QtWidgets.QHBoxLayout()
        self.parameterLayout.addWidget(self.estimatedPlanesWidget)

        self.box.addLayout(self.parameterLayout)

        self.setLayout(self.box)

    def resetValues(self):
        defaultSettings = resetSettings()

        self.estimatedPlanesWidget.resetValue(defaultSettings)