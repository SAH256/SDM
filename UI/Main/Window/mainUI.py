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

    def __init__(self):
        super().__init__()

        self.windowLayout = QtWidgets.QBoxLayout(Dir.TopToBottom)
        self.setLayout(self.windowLayout)

        self.mainLayout = QtWidgets.QBoxLayout(Dir.LeftToRight)
        self.windowLayout.addLayout(self.mainLayout)

        self._left_menu()
        self._content()
        self._right_menu()

        self.windowLayout.setContentsMargins(5, 5, 5, 5)


    def _left_menu(self):
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)

        self.toolBar = ToolBar()
        self.leftLayout.addWidget(self.toolBar)

        self.__category()
        self.toolBar.add_space(1)
        self.__tool()


    def __category(self):
        self.categoryTab = OptionTab(Dir.TopToBottom)
        self.toolBar.add_action(self.categoryTab)


    def __tool(self):
        self.toolTab = ToolControl(Dir.TopToBottom)
        self.toolBar.add_action(self.toolTab)


    def _content(self):
        self.conLayout = QtWidgets.QBoxLayout(Dir.TopToBottom)
        self.mainLayout.addLayout(self.conLayout)

        self.__header()
        self.__list()


    def __header(self):
        headLayout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(headLayout)

        self.headerTab = HeaderControl()
        headLayout.addWidget(self.headerTab)


    def __list(self):
        listLayout = QtWidgets.QHBoxLayout()
        self.conLayout.addLayout(listLayout, 1)

        self.taskList = View()

        listLayout.addWidget(self.taskList, 1)


    def _right_menu(self):
        rightLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(rightLayout)

        self.btnBar = ToolBar()
        rightLayout.addWidget(self.btnBar)

        self.btnBar.add_space(1)
        self.__action()
        self.btnBar.add_space(1)


    def __action(self):
        self.actionTab = ToolControl(Dir.TopToBottom)

        self.btnBar.add_action(self.actionTab)


