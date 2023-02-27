from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from widgets.components.buttonTable import ButtonTable
from PyQt5 import QtCore, QtGui
from utils import updateClass
class ResultTable(QTableWidget):
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        super(ResultTable, self).__init__(len(self.data), len(self.data[0]))
        
        self.verticalHeader().setVisible(False)
        self.setObjectName("resultTable")
       
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setObjectName("resultTableHeader")
        self.itemChanged.connect(self.itemChangedEvent)
 
    def setData(self): 
        for i in range(len(self.data)):
            item_segment = QTableWidgetItem(self.data[i]["Segment"])
            item_segment.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
            item_segment.setText(self.data[i]["Segment"])

            item_area = QTableWidgetItem(self.data[i]["Surface area"])
            item_area.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
            item_area.setText(self.data[i]["Surface area"])
   
            self.setItem(i, 0, item_segment)
            self.setItem(i, 1, item_area)
            rgb = [int(float(x) * 255) for x in self.data[i]["rgb"][1:-1].split(" ")]
            self.setCellWidget(i, 2, ButtonTable(self.data[i], self.parent, rgb))

        headers = list(self.data[0].keys())
        headers[-1] = ""
        self.setHorizontalHeaderLabels(headers)
    
    def itemChangedEvent(self, item):
        columns = range(self.columnCount())
        rows = range(self.rowCount())
        for column in columns:
            for row in rows:
                if item == self.item(row, column):
                    updateClass(row, column, item.text())