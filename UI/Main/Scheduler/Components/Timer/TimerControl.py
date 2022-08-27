from Utility.Core import QUEUE

from .TimerUI import TimerUI


# Timer setting widget in scheduler for a queue -- Control class
class TimerControl(TimerUI):

    def __init__(self):
        super().__init__()

        self.data = None

        self.__connect_slots()


    def __connect_slots(self):
        self.start_timer.toggled.connect(self.__basis_handler)


    def apply(self):

        start = self.start_timer.get_data()
        stop = self.stop_timer.get_data()
        date = self.date_option.get_data()

        if not start and QUEUE.TIMER.DATE in date:
            date[QUEUE.TIMER.DATE] = None


        if self.data:
            self.data.start_time = start
            self.data.timer_basis = date
            self.data.stop_time = stop


    def __basis_handler(self, s):
        self.date_option.setEnabled(s)


    def set_data(self, data):
        self.data = data
        self.__setup()


    def set_queue_type(self, _type):
        self.date_option.set_queue_type(_type)


    def __setup(self):

        if self.data:
            self.start_timer.set_data(self.data.start_time)
            self.date_option.set_data(self.data.timer_basis)
            self.stop_timer.set_data(self.data.stop_time)


    def _reset(self):
        self.__setup()



