import colorsys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
from widgets.components.buttonTable import ButtonTable

class ResultTable(QTableWidget):
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        
        super(ResultTable, self).__init__(len(self.data), len(self.data[0]) + 1)
        #QTableWidget.__init__(self, 4 , 3)
        
        self.verticalHeader().setVisible(False)
        self.setObjectName("resultTable")
        
        #header = header = self.horizontalHeader() 
        #for i in range(len(self.data[0])):
        #    header.setSectionResizeMode(i,  QHeaderView.ResizeMode.Stretch)
        #header.setSectionResizeMode(len(self.data[0]) + 1, QHeaderView.ResizeMode.ResizeToContents)
 
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setObjectName("resultTableHeader")
 
    def setData(self): 
        for i in range(len(self.data)):
            self.setItem(i, 0, QTableWidgetItem(f'Segment {self.data[i]["Segment"]}'))
            self.setItem(i, 1, QTableWidgetItem(self.data[i]["Class"]))
            self.setItem(i, 2, QTableWidgetItem(self.data[i]["Surface area"]))
            self.setCellWidget(i, 3, ButtonTable(self.data[i], self.parent))
        headers = list(self.data[0].keys())
        headers.append("")
        self.setHorizontalHeaderLabels(headers)