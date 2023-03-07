from PyQt5 import QtWidgets

class CheckMerge(QtWidgets.QCheckBox):
    def __init__(self, parent, segment_id):
        super(CheckMerge, self).__init__()
        self.parent = parent
        self.segment_id = segment_id
        self.stateChanged.connect(lambda: self.parent.checkChanged(self.segment_id))