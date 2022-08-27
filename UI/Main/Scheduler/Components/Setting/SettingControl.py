from Utility.Core import QUEUE

from .SettingUI import SettingUI


# Setting widget in Scheduler for a queue -- Control class
class Setting(SettingUI):

    def __init__(self):
        super().__init__()

        self.data = None


    def set_data(self, data):

        if data:
            self.data = data

            self.__setup()


    def __setup(self):

        s = QUEUE.SETTING

        self.typeOption.setEnabled(self.data.creator_type == s.USER_TYPE)

        self.name.setText(self.data.name)
        self.typeOption.setCurrentIndex(self.data.timer_type)
        self.concurrent.set_value(self.data.concurrent)
        self.retry.set_value(self.data.retry)

        self.startup.setChecked(self.data.startup)


    def apply(self):
        self.data.concurrent = self.concurrent.get_value()
        self.data.retry = self.retry.get_value()
        self.data.startup = self.startup.isChecked()

        if self.typeOption.isEnabled():
            self.data.timer_type = self.typeOption.currentIndex()
