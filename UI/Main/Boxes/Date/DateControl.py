from Utility.Core import QUEUE

from .DateUI import DateUI


# Date select widget -- Control class
class DateControl(DateUI):

    def __init__(self):
        super().__init__()

        self.queue_type = None

        self.data = None
        self.optionCombo.addItems(QUEUE.TIMER.TIMER_BASIS)

        self.__connect_slots()


    def __connect_slots(self):
        self.optionCombo.currentIndexChanged.connect(self.__change_stack)


    def __change_stack(self, index):
        self.stackLayout.setCurrentIndex(index)
        self.__toggle_repeat(index)


    def set_queue_type(self, _type):
        self.queue_type = _type

        if _type == QUEUE.SETTING.PERIODIC:
            index = self.WEEK_INDEX
            self.optionCombo.setCurrentIndex(index)

        self.optionCombo.setEnabled(_type != QUEUE.SETTING.PERIODIC)


    def get_data(self):

        base = self.optionCombo.currentIndex()
        wid = self.stackLayout.widget(base)

        date = None
        r = None
        days = None

        if base == self.CALENDAR_INDEX:
            date = wid.get_data()

        else:
            if self.queue_type == QUEUE.SETTING.PERIODIC:
                r = self.repeat.get_data()

            days = wid.get_data()


        return {
            QUEUE.TIMER.DATE : date,
            QUEUE.TIMER.REPEAT : r,
            QUEUE.TIMER.DAY : days,
        }


    def set_data(self, data):
        self.__reset()

        self.data = data

        self.__setup()


    def __reset(self):
        for i in range(self.stackLayout.count()):
            self.stackLayout.widget(i).reset()


    def __setup(self):

        date = self.data.get(QUEUE.TIMER.DATE)
        repeat = self.data.get(QUEUE.TIMER.REPEAT)
        day = self.data.get(QUEUE.TIMER.DAY)
        index = None

        if date:
            index = self.CALENDAR_INDEX
            wid = self.stackLayout.widget(index)
            wid.set_data(date)

        elif day:
            index = self.WEEK_INDEX
            wid = self.stackLayout.widget(index)

            self.repeat.set_data(repeat)
            wid.set_data(day)

        if not index:
            index = self.CALENDAR_INDEX if QUEUE.SETTING.ONE_TIME == self.queue_type else self.WEEK_INDEX

        self.optionCombo.setCurrentIndex(index)
        self.__toggle_repeat(index)


    def __toggle_repeat(self, index):
        self.repeat.setVisible(index == self.WEEK_INDEX and self.queue_type != QUEUE.SETTING.ONE_TIME)


