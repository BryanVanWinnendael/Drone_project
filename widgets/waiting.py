from PyQt5 import QtCore, QtWidgets


class WaitingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)

        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Loading...")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(self.label, 0, 0, 1, 1)

        self.setLayout(layout)


        
    