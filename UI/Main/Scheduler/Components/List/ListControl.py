from PyQt5.QtCore import pyqtSignal

from UI.Main.Popup.PopupControl import create_popup

from Utility.Core import POPUP_TYPE

from .ListUI import ListUI


# Queue list widget in Scheduler -- UI class
class List(ListUI):

    item_changed = pyqtSignal(str)
    item_manager = pyqtSignal(str, bool)
    queue_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.info = None

        self.__connect_slots()


    def __connect_slots(self):
        self.view.current_changed.connect(self.__change_handler)
        self.view.item_dragged.connect(self.__drag_handler)
        self.addBtn.clicked.connect(self.__add_handler)
        self.removeBtn.clicked.connect(self.__remove_handler)


    def __setup(self):

        if self.info:
            self.view.add_data([x[:2] for x in self.info])


    def set_info(self, data):
        self.info = data
        self.__setup()


    def __change_handler(self, name):
        self.item_changed.emit(name)

        for item in self.info:
            if item[0] == name:
                self.__enable_btn(not item[2])


    def __add_handler(self):
        _type = POPUP_TYPE.ADD
        title = 'Enter New Queue Name'
        data = ['Queue', [x[0] for x in self.info]]

        result = create_popup(self, _type, title, None, data)

        if result:
            self.item_manager.emit(result, True)


    def __remove_handler(self):
        _type = POPUP_TYPE.CONFIRMATION
        title = 'Delete Queue'
        name = self.view.selected_item()

        result = create_popup(self, _type, title, data = name)

        if result:
            self.view.remove_item(name)
            self.item_manager.emit(name, False)


    def __enable_btn(self, s):
        self.removeBtn.setEnabled(s)


    def __drag_handler(self, data):
        self.queue_changed.emit(data)



