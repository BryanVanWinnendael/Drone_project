from PyQt5 import QtCore, QtGui, QtWidgets

from utils import getSettings, resetSettings, saveSettings, saveRecentFile, clusterStrategies

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
    def __init__(self, settings, value, info):
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

class ButtonSettings(QtWidgets.QToolButton):
    def __init__(self):
        super(ButtonSettings, self).__init__()
        self.settings = getSettings()
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.setIcon(QtGui.QIcon('assets/settings.svg'))
        self.setIconSize(QtCore.QSize(30, 30))
        self.setGeometry(QtCore.QRect(220, 120, 41, 41))
        self.setObjectName("buttonSettings")
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        widget = QtWidgets.QWidget()
        widgetLayout = QtWidgets.QVBoxLayout(widget)
        widgetLayout.setSpacing(20)

        self.treshholdWidget = TextInput(self.settings, 'Treshold', 'Treshold is the minimum value of the point cloud to be rendered. The higher the value, the less points will be rendered.')
        self.neigboursWidget = TextInput(self.settings, 'Number of neigbours', 'number')
        self.iterationsWidget = TextInput(self.settings, 'Iterations * 100', 'number')
        self.minRatioWidget = TextInput(self.settings, 'Min. ratio', 'number')
        self.strategyWidget = DropDown(clusterStrategies, "Cluster strategy", "info cluster strategy", self.settings)

        widgetLayout.addWidget(self.strategyWidget)
        widgetLayout.addWidget(self.treshholdWidget)
        widgetLayout.addWidget(self.neigboursWidget)
        widgetLayout.addWidget(self.iterationsWidget)
        widgetLayout.addWidget(self.minRatioWidget)

        resetButton = QtWidgets.QPushButton('Reset')
        resetButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        resetButton.setObjectName('buttonReset')
        resetButton.setMinimumHeight(30)
        resetButton.clicked.connect(self.resetSettingsValue)
        widgetLayout.addWidget(resetButton)

        widgetAction = QtWidgets.QWidgetAction(self)
        widgetAction.setDefaultWidget(widget)

        widgetMenu = QtWidgets.QMenu(self)
        widgetMenu.setMinimumWidth(300)
        widgetMenu.addAction(widgetAction)
        self.setMenu(widgetMenu)
    
    def resetSettingsValue(self):
        defaultSettings = resetSettings()

        self.treshholdWidget.resetValue(defaultSettings)
        self.neigboursWidget.resetValue(defaultSettings)
        self.iterationsWidget.resetValue(defaultSettings)