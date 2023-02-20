from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie
class WaitingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)

        self.centralwidget = QtWidgets.QWidget(self)

        self.labelGif = QtWidgets.QLabel(self.centralwidget)
        self.labelGif.setGeometry(QtCore.QRect(25, 25, 200, 200))
        self.labelGif.setMinimumSize(QtCore.QSize(200, 200))
        self.labelGif.setMaximumSize(QtCore.QSize(200, 200))
        self.labelGif.setObjectName("label")

        self.movie = QMovie("assets/loading.gif")
        self.labelGif.setMovie(self.movie)
        self.movie.start()

        layout.addWidget(self.labelGif, 0, 0, 1, 1)

        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Loading...")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.label.setMaximumHeight(30)
        self.label.setMinimumWidth(200)
        layout.addWidget(self.label, 1, 0, 1, 1)

        self.setLayout(layout)


        
    