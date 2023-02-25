from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtWidgets, QtCore, QtGui
from utils import getSettings, saveSettings, resetSettings

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
        widgetLabel = QtWidgets.QLabel('Popup Text')
        self.widgetValue = QtWidgets.QDoubleSpinBox()
        self.widgetValue.setValue(self.settings['value'])

        resetButton = QtWidgets.QPushButton('Reset')
        resetButton.clicked.connect(self.resetSettingsValue)

        widgetLayout.addWidget(widgetLabel)
        widgetLayout.addWidget(self.widgetValue)
        widgetLayout.addWidget(resetButton)

        widgetAction = QtWidgets.QWidgetAction(self)
        widgetAction.setDefaultWidget(widget)

        widgetMenu = QtWidgets.QMenu(self)
        widgetMenu.addAction(widgetAction)
        self.setMenu(widgetMenu)

        self.widgetValue.valueChanged.connect(self.saveSettingsValue)
    
    def resetSettingsValue(self):
        defaultSettings = resetSettings()
        self.widgetValue.setValue(defaultSettings['value'])

    def saveSettingsValue(self):
        self.settings['value'] = self.widgetValue.value()
        saveSettings(self.settings)
