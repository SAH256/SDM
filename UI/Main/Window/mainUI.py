from PyQt5 import QtWidgets, QtCore, QtGui

from UI.Main.Tab.Header.HeaderControl import HeaderControl
from UI.Main.Tab.Tool.ToolControl import ToolControl
from UI.Main.Tab.Option.OptionTab import OptionTab
from UI.Main.Bar.ToolBar import ToolBar
from UI.Main.List.TaskList import View


class Dir:
    LeftToRight = QtWidgets.QBoxLayout.Direction.LeftToRight
    RightToLeft = QtWidgets.QBoxLayout.Direction.RightToLeft
    TopToBottom = QtWidgets.QBoxLayout.Direction.TopToBottom
    BottomToTop = QtWidgets.QBoxLayout.Direction.BottomToTop



# Main window central widget -- UI class
class MainUI(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.mainLayout = QtWidgets.QBoxLayout(Dir.TopToBottom)
        self.setLayout(self.mainLayout)

        self._top()
        self._content()

        self.mainLayout.setContentsMargins(0, 0, 0, 0)


    def _top(self):
        self.topLayout = QtWidgets.QVBoxLayout()
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(self.topLayout)
        
        self.__header()


    def __header(self):
        headLayout = QtWidgets.QHBoxLayout()
        self.topLayout.addLayout(headLayout)

        self.headerTab = HeaderControl(self)
        headLayout.addWidget(self.headerTab)


    def _content(self):
        self.conLayout = QtWidgets.QBoxLayout(Dir.LeftToRight)
        self.conLayout.setContentsMargins(2, 5, 2, 5)
        self.mainLayout.addLayout(self.conLayout)

        self.__left_bar()
        self.__list()
        self.__right_bar()


    def __left_bar(self):
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.conLayout.addLayout(self.leftLayout)

        self.toolBar = ToolBar(self)
        self.leftLayout.addWidget(self.toolBar)

        self.__category()
        self.toolBar.add_space(1)
        self.__tool()


    def __category(self):
        self.categoryTab = OptionTab(self, Dir.TopToBottom)
        self.toolBar.add_action(self.categoryTab)


    def __tool(self):
        self.toolTab = ToolControl(self, Dir.TopToBottom)
        self.toolBar.add_action(self.toolTab)


    def __list(self):
        listLayout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(listLayout)

        self.taskList = View(self)

        listLayout.addStretch(1)
        listLayout.addWidget(self.taskList, 6)
        listLayout.addStretch(1)


    def __right_bar(self):
        rightLayout = QtWidgets.QVBoxLayout()
        self.conLayout.addLayout(rightLayout)

        self.btnBar = ToolBar(self, False)
        rightLayout.addWidget(self.btnBar)

        self.btnBar.add_space(1)
        self.__action()
        self.btnBar.add_space(1)


    def __action(self):
        self.actionTab = ToolControl(self, Dir.TopToBottom)

        self.btnBar.add_action(self.actionTab)


