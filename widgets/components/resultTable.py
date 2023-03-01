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
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setObjectName("resultTableHeader")
        self.itemChanged.connect(self.itemChangedEvent)
 
    def setData(self): 
        self.setRowCount(len(self.data))
        for i in range(len(self.data)):
            self.addResultRow(i)

        headers = list(self.data[0].keys())
        headers.insert(0, "")
        headers[-1] = ""
        self.setHorizontalHeaderLabels(headers)
    
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
                if len(self.parent.getSelectedPoints()) == 0:
                    self.parent.deleteButton.hide()
                    self.parent.deleteButton.setEnabled(False)
        else:
            self.checkedButtons.append(segment_id)
            self.parent.mergeBtn.show()
            self.parent.deleteButton.show()
            self.parent.deleteButton.setEnabled(True)

    def mergeSegments(self):
        merger = Merger(self.parent)
        merger.mergeSegments(self.checkedButtons, self.parent.getRenderedFile())
        self.clearChecks()
        self.parent.dataChanged()
        self.setRowCount(len(self.data))
        self.addResultRow(len(self.data) - 1)

    def addResultRow(self, row_number):
        new_data = self.data[row_number]
        item_segment = QTableWidgetItem(new_data["Segment"])
        item_segment.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
        item_segment.setText(new_data["Segment"])

        item_class = QTableWidgetItem(new_data["Class"])
        item_class.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
        item_class.setText(new_data["Class"])

        item_area = QTableWidgetItem(new_data["Surface area"])
        item_area.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
        item_area.setText(new_data["Surface area"])

        self.setCellWidget(row_number, 0, CheckMerge(self, int(new_data["Segment"])))
        self.setItem(row_number, 1, item_segment)
        self.setItem(row_number, 2, item_class)
        self.setItem(row_number, 3, item_area)
        rgb = [int(x) for x in new_data["rgb"][1:-1].split(",")]
        self.setCellWidget(row_number, 4, ButtonTable(new_data, self.parent, rgb))