from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt



# Combo delegate for priority column in file tree
class Combo(QtWidgets.QStyledItemDelegate):
    ITEMS = ['Low', 'Normal', 'High']
    last_connection = None

    FONT = QtGui.QFont()
    FONT.setPointSize(8)
    
    data_changed = QtCore.pyqtSignal(str)


    def createEditor(self, parent, option, index):
        wid = QtWidgets.QComboBox(parent)
        wid.addItems(self.ITEMS)

        wid.setFont(self.FONT)

        QtCore.QTimer.singleShot(50, wid.showPopup)

        return wid
    

    def setEditorData(self, editor, index):
        
        value = index.model().data(index, Qt.ItemDataRole.EditRole)

        if value:
            editor.setCurrentText(value)
            self.last_connection = editor.currentTextChanged.connect(self.data_changed.emit)


    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.ItemDataRole.EditRole)

    
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


    def destroyEditor(self, editor, index):
        super().destroyEditor(editor, index)
        editor.currentIndexChanged.disconnect(self.last_connection)
        self.last_connection = None


    def paint(self, painter, option, index):
        super().paint(painter, option, index)



        st = QtWidgets.QApplication.style()
        if option.widget:
            st = option.widget.style()
        
        file = index.model().itemFromIndex(index).is_file()


        if file:
        
            style = QtWidgets.QStyleOptionComboBox()
            style.rect = option.rect
            style.state = option.state
            style.editable = False
            style.currentText = index.data(Qt.ItemDataRole.DisplayRole)
            style.popupRect = option.rect

            if style.state & QtWidgets.QStyle.StateFlag.State_MouseOver:
                style.state ^= QtWidgets.QStyle.StateFlag.State_MouseOver

            st.drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_ComboBox, style, painter)

        op = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(op, index)
        op.rect.setX(op.rect.x() + 1)
        

        if op.state & QtWidgets.QStyle.StateFlag.State_Selected:
            op.state ^= QtWidgets.QStyle.StateFlag.State_Selected

        st.drawControl(QtWidgets.QStyle.ControlElement.CE_ItemViewItem , op, painter)
    


















