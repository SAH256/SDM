from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from UI.Base.Items.BaseItem import BaseItem

from UI.Base.Label.ElideLabel import Elide


# Task Item UI class for representing a task in task list



class TaskItem(BaseItem):

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.mainLayout.setContentsMargins(5, 5, 10, 5)

        self.expanded = False

        self.line_width = 2
        self.normal_size = 16
        self.big_size = 32

        self._info()

        self.__set_style()


    def _info(self):
        self.infoLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self.mainLayout.addLayout(self.infoLayout)
        self.mainLayout.setStretchFactor(self.infoLayout, 1)

        self.__name()
        self.__monitor()


    def __name(self):
        nameLayout = QtWidgets.QHBoxLayout()
        nameLayout.setContentsMargins(0, 5, 0, 0)
        self.infoLayout.addLayout(nameLayout, 2)
        
        data = [
            ('nameLabel', 'name', Elide),
            None,
            ('status', 'status', QtWidgets.QLabel),
        ]

        for item in data:
            if item:
                wid = item[2](self)
                wid.setObjectName(item[1])

                nameLayout.addWidget(wid)
                setattr(self, item[0], wid)
            else:
                nameLayout.addStretch(1)


    def __monitor(self):
        self.monLayout = QtWidgets.QHBoxLayout()
        self.monLayout.setContentsMargins(0, 5, 0, 5)
        self.infoLayout.addLayout(self.monLayout)

        cells = [
            ('progress', '756 MB / 1,99 GB', 120),
            1, 
            ('percentage', '(35.00%)', None),
            10,
            ('remained_time', '5m 16s', None)
        ]

        for cell in cells:

            if type(cell) == int:
                self.monLayout.addStretch(cell)
            
            else:
                temp_wid = QtWidgets.QLabel(cell[1])
                temp_wid.setObjectName(cell[0])

                if cell[2]:
                    temp_wid.setFixedWidth(cell[2])

                temp_wid.setVisible(self.expanded)
                self.monLayout.addWidget(temp_wid)

                setattr(self, cell[0], temp_wid)

    
    def _expand(self):
        self.expanded = True
        self.__change_view()

    def _collapse(self):
        self.expanded = False
        self.__change_view()

    def __change_view(self):

        if self.expanded:
            self.infoLayout.setDirection(self.infoLayout.Direction.TopToBottom)
            self.infoLayout.setStretch(0, 0)
        else:
            self.infoLayout.setDirection(self.infoLayout.Direction.LeftToRight)
            self.infoLayout.setStretch(0, 2)

        self.progress.setVisible(self.expanded)
        self.percentage.setVisible(self.expanded)
        self.remained_time.setVisible(self.expanded)


    def __set_style(self):
        style = '''

        #item {
            background-color : white;
        }

        QLabel {
            color : #455;
        }


        #name {
            font-family : Arial;
            font-size : 15px;
            font-weight : 600;
            color : #e52c2c;
        }

        
        #name[css-class="resume"] {
            color : #23af27;
        }
        

        '''

        self.setStyleSheet(style)





