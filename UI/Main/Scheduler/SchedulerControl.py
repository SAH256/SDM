
from PyQt5.QtCore import QTimer

from .SchedulerUI import SchedulerUI

from Utility.Core import QUEUE


# Scheduler dialog for managing queues -- Control class
class Scheduler(SchedulerUI):

    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.queues = self.manager.get_queues()

        self.current_index = 0
        self.current_item = None

        self.__connect_slots()
        self.__toggle_btn()

        self.__setup()


    def __connect_slots(self):

        self.queueList.item_changed.connect(self.__change_data)
        self.queueList.item_manager.connect(self.__manager_handler)
        self.queueList.queue_changed.connect(self.__queue_handler)

        self.tab.item_changed.connect(self.__stack_change)

        self.startBtn.clicked.connect(self.__start_handler)

        self.applyBtn.clicked.connect(self.__apply_handler)
        self.closeBtn.clicked.connect(self.close)


    def __stack_change(self, index):
        self.stackLayout.setCurrentIndex(index)
        self.current_index = index

        if index == self.TIMER_INDEX:
            self.timerOption.set_queue_type(self.current_item.get_timer_type())
            self.timerOption._reset()


    def __setup(self):
        self.queueList.set_info(self.manager.get_info())


    def __change_data(self, name):
        item = self.queues.get(name)
        self.current_item = item

        if item:
            self.timerOption.set_queue_type(item.get_timer_type())

            self.timerOption.set_data(item.timer)
            self.fileOption.set_data(item.files)
            self.processOption.set_data(item.process)
            self.settingOption.set_data(item.setting)

        self.__toggle_btn()


    def __apply_handler(self):
        self.timerOption.apply()
        self.processOption.apply()
        self.settingOption.apply()

        self.__setup()
        self.current_item.setup_timer()


    def __manager_handler(self, name, created = True):

        if created:
            self.manager.create_queue(name, creator_type = QUEUE.SETTING.USER_TYPE)
        else:
            self.manager.remove_queue(name)

        self.__setup()


    def __queue_handler(self, data):

        if data:
            source = data[0]
            dest = data[1]
            items = data[2]

            self.manager.change_queue(source, dest, items)


    def __start_handler(self):
        if self.current_item:
            if self.current_item.is_running():
                self.current_item.stop_action()
            else:
                self.current_item.start_action()
            
            self.__toggle_btn()


    def __toggle_btn(self):
        txt = 'Start'
        if self.current_item and self.current_item.is_running():
            txt = 'Stop'

        if self.startBtn.text() != txt:
            self.startBtn.setText(txt)

