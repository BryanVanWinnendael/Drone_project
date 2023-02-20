from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WaitingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)

        self.labelGif = QtWidgets.QLabel()
        self.movie = QMovie("assets/loading.gif")
        
        size = self.movie.scaledSize()
        self.labelGif.setScaledContents(True)
        
        self.labelGif.setGeometry(0, 0, 50, 50)
        self.labelGif.setMinimumSize(QtCore.QSize(50, 50))
        self.labelGif.setMaximumSize(QtCore.QSize(50, 50))
        self.labelGif.setObjectName("label")
        

        self.labelGif.setMovie(self.movie)
        self.labelGif.movie()
        self.movie.start()
        self.labelGif.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.labelGif, 0, 0)

        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Loading...")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.label.setMaximumHeight(30)
        self.label.setMinimumWidth(200)

        layout.addWidget(self.label, 1, 0)
        self.setLayout(layout)


        
    