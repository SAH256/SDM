from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from UI.Base.Button.StyledButton import StyleButton
from UI.Base.Input.StyledInput import StyleInput

from Utility.Core import ICONS


# Spin Box UI style class



class SpinBox(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        self.setLayout(self.mainLayout)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        name = 'spinbox'
        self.setObjectName(name)

        p = QtWidgets.QSizePolicy()
        p.setHorizontalPolicy(p.Policy.Minimum)
        p.setVerticalPolicy(p.Policy.Fixed)
        self.setSizePolicy(p)

        w = 30
        self.setMaximumWidth(w)
        

        self._up_btn()
        self._box()
        self._down_btn()

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addStretch(1)


    def _up_btn(self):
        upLayout = QtWidgets.QHBoxLayout()
        upLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(upLayout)

        self.upBtn = StyleButton(ICONS.OTHER.ADD_2, '')
        self.upBtn.setMaximumHeight(15)
        self.upBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        upLayout.addWidget(self.upBtn)


    def _box(self):
        boxLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(boxLayout)
        
        name = 'spinbox-input'

        self.numBox = StyleInput()
        self.numBox.setObjectName(name)
        self.numBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.numBox.setClearButtonEnabled(False)
        a = QtGui.QIntValidator(0, 9999)
        
        self.numBox.setValidator(a)
        self.numBox.set_double(True)

        boxLayout.addWidget(self.numBox)
        

    def _down_btn(self):
        downLayout = QtWidgets.QHBoxLayout()
        downLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(downLayout)

        self.downBtn = StyleButton(ICONS.OTHER.SUB, '')
        self.downBtn.setMaximumHeight(15)
        self.downBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        downLayout.addWidget(self.downBtn)
