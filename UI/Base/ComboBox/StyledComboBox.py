from PyQt5 import QtWidgets

class ComboBox(QtWidgets.QComboBox):
    
    def __init__(self):
        super().__init__()

        self.delegate = QtWidgets.QStyledItemDelegate()
        self.setItemDelegate(self.delegate)
        
        name = 'combo-box'
        self.setObjectName(name)
        
    def _reset(self):
        self.setCurrentIndex(0)


    def setEditable(self, s):
        super().setEditable(s)
        self.lineEdit().setClearButtonEnabled(s)
