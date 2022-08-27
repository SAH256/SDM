
from PyQt5.QtCore import QTimer

from .FileUI import FileUI


# File view for managing tasks in a queue -- Control class
class File(FileUI):

    def __init__(self):
        super().__init__()
    
        self.data = None

        self.__connect_slots()


    def __connect_slots(self):
        self.upBtn.clicked.connect(self.__up_handler)
        self.downBtn.clicked.connect(self.__down_handler)
        self.delBtn.clicked.connect(self.__del_handler)


    def set_data(self, data):
        self.data = data
        self.__setup()


    def __setup(self):
        self.table._reset()

        for info in self.data.get_info():
            self.table.create_row(info)

        self.__setup_timer()


    def __setup_timer(self):
        self.__update_timer = QTimer()
        self.__update_timer.setSingleShot(False)
        self.__update_timer.timeout.connect(self.__update_handler)
        self.__update_timer.start(250)


    def __up_handler(self):
        order = self.table.move_selected()

        if order:
            self.data.change_order(order)


    def __down_handler(self):
        order = self.table.move_selected(False)

        if order:
            self.data.change_order(order)


    def __del_handler(self):
        removed = self.table.remove_selected()

        if removed:
            self.data.remove_tasks(removed)


    def __update_handler(self):
        self.table._update_info()

