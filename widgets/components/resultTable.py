from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
import csv
import open3d as o3d
from widgets.components.buttonTable import ButtonTable

class ResultTable(QTableWidget):
    def __init__(self, parent):
        self.parent = parent
        file = open("data/results/output.csv", "r")
        self.data = list(csv.DictReader(file, delimiter=","))
        file.close()

        super(ResultTable, self).__init__(len(self.data), len(self.data[0]) + 1)
        #QTableWidget.__init__(self, 4 , 3)
        
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): 
        for i in range(len(self.data)):
            self.setItem(i, 0, QTableWidgetItem(self.data[i]["Segment"]))
            self.setItem(i, 1, QTableWidgetItem(self.data[i]["Surface area"]))
            self.setCellWidget(i, 2, ButtonTable(self.data[i], self.parent))
        headers = list(self.data[0].keys())
        headers.append("View")
        self.setHorizontalHeaderLabels(headers)