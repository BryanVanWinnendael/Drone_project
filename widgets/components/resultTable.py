from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox
from widgets.components.buttonTable import ButtonTable
from widgets.components.checkMerge import CheckMerge
from PyQt5 import QtCore, QtGui
from utils import updateClass
from model.merger import Merger
class ResultTable(QTableWidget):
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        super(ResultTable, self).__init__(len(self.data), len(self.data[0]) + 1)

        self.checkedButtons = []
        self.verticalHeader().setVisible(False)
        self.setObjectName("resultTable")
       
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setObjectName("resultTableHeader")
        self.itemChanged.connect(self.itemChangedEvent)
 
    def setData(self): 
        self.setRowCount(len(self.data))
        for i in range(len(self.data)):
            item_segment = QTableWidgetItem(self.data[i]["Segment"])
            item_segment.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
            item_segment.setText(self.data[i]["Segment"])

            item_class = QTableWidgetItem(self.data[i]["Class"])
            item_class.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
            item_class.setText(self.data[i]["Class"])
            print(self.data[i]["Class"])

            item_area = QTableWidgetItem(self.data[i]["Surface area"])
            item_area.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
            item_area.setText(self.data[i]["Surface area"])
   
            self.setCellWidget(i, 0, CheckMerge(self, int(self.data[i]["Segment"])))
            self.setItem(i, 1, item_segment)
            self.setItem(i, 2, item_class)
            self.setItem(i, 3, item_area)
            rgb = [int(x) for x in self.data[i]["rgb"][1:-1].split(",")]
            self.setCellWidget(i, 4, ButtonTable(self.data[i], self.parent, rgb))

        headers = list(self.data[0].keys())
        headers.insert(0, "")
        headers[-1] = ""
        self.setHorizontalHeaderLabels(headers)
        self.update()
    
    def itemChangedEvent(self, item):
        columns = range(self.columnCount())
        rows = range(self.rowCount())
        for column in columns:
            for row in rows:
                if item == self.item(row, column):
                    updateClass(row, column, item.text())

    def clearChecks(self):
        rows = range(self.rowCount())
        for i in rows:
            self.cellWidget(i, 0).setChecked(False)
    
    def checkChanged(self, segment_id):
        if segment_id in self.checkedButtons:
            self.checkedButtons.remove(segment_id)
            if len(self.checkedButtons) == 0:
                # Hide merge button
                self.parent.mergeBtn.hide()
        else:
            self.checkedButtons.append(segment_id)
            self.parent.mergeBtn.show()

    def mergeSegments(self):
        merger = Merger()
        merger.mergeSegments(self.checkedButtons)
        self.clearChecks()
        self.parent.dataChanged()