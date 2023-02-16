from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
import csv
import open3d as o3d
from widgets.components.buttonTable import ButtonTable

class ResultTable(QTableWidget):
    def __init__(self):

        file = open("data/results.csv", "r")
        self.data = list(csv.DictReader(file, delimiter=","))
        file.close()

        super(ResultTable, self).__init__(len(self.data), 4)
        #QTableWidget.__init__(self, 4 , 3)
        
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): 
        for i in range(len(self.data)):
            
            self.setItem(i, 0, QTableWidgetItem(self.data[i]["name"]))
            self.setItem(i, 1, QTableWidgetItem(self.data[i]["id"]))
            self.setItem(i, 2, QTableWidgetItem(self.data[i]["area"]))
            self.setCellWidget(i, 3, ButtonTable(self.data[i], self))
        self.setHorizontalHeaderLabels(["Name", "Id", "Area", "View"])