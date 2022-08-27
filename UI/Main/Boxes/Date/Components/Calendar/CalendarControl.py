import datetime as dt

from .CalendarUI import CalendarUI

from .Popup import Popup


class CalendarControl(CalendarUI):

    def __init__(self):
        super().__init__()

        self.date = dt.date.today()
        self.__pattern = "%A %d %b, %Y"

        self.__connect_slots()
        self.__update_txt()
    

    def __connect_slots(self):
        self.calBtn.clicked.connect(self.__calender_handler)

        self.dateCombo.setText(' ')
        self.dateCombo.setEnabled(False)



    def __calender_handler(self):
        d = Popup(self.date)
        self.date = d.exec()
        
        self.__update_txt()
    

    def __update_txt(self):
        txt = self.date.strftime(self.__pattern)
        self.dateCombo.setText(txt)
        


    def get_data(self):
        return self.date.isoformat()

    def set_data(self, date_iso):

        if date_iso:
            self.date = dt.date.fromisoformat(date_iso)
        self.__update_txt()


    def reset(self):
        today = dt.date.today()
        self.set_data(today.isoformat())







