from PyQt5 import QtWidgets

class ComboBox(QtWidgets.QComboBox):
    
    def __init__(self):
        super().__init__()

        self.delegate = QtWidgets.QStyledItemDelegate()
        self.setItemDelegate(self.delegate)
            
        self.__apply_style()
        
    def _reset(self):
        self.setCurrentIndex(0)


    def setEditable(self, s):
        super().setEditable(s)
        self.lineEdit().setClearButtonEnabled(s)

    def __apply_style(self):
        style = '''
            QComboBox {
                border : none;
                background-color : #eee;
                padding : 5px 10px;
                /* min-width : 6em; */
            }

            QComboBox:on,
            QComboBox:editable {
                border-bottom : 2px solid blue;

                background-color : #fff;
            }

            QComboBox::drop-down {
                width : 25px;
                height : 25px;

                border : none;

                subcontrol-origin : padding;
                subcontrol-position: top right;

            }

            * {
                background-color : white;
            }

            QComboBox QAbstractItemView {

                border : 1px solid gray;
                background-color : #ddd;
                outline : none;
            }

            QComboBox QAbstractItemView::item {
                padding : 3px 5px;
            }

            
            QComboBox::down-arrow {
                image : url(assets/Icons/Default/Other/arrow-closed.png);
                width : 10px;
                height : 10px;
            }
            
            QComboBox::down-arrow:on {
                image : url(assets/Icons/Default/Other/arrow-open.png);
                
            }

        '''
            
        self.setStyleSheet(style)


