
from PyQt5 import QtCore
from .AuthUI import AuthUI


# Mini authentication input widget -- Control class
class AuthControl(AuthUI):

    authChanged = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setChecked(False)
        self.__connect_slots()


    def __connect_slots(self):
        self.username.textChanged.connect(self.check_auth)
        self.password.textChanged.connect(self.check_auth)


    def check_auth(self):
        user = self.get_user()
        wrd = self.get_password()

        user_state = ''
        wrd_state = ''

        if wrd and not user:
            user_state = 'error'

        if user and not wrd:
            wrd_state = 'error'

        self.username.setObjectName(user_state)
        self.password.setObjectName(wrd_state)

        self.authChanged.emit()

    def get_user(self):
        return self.username.text()


    def get_password(self):
        return self.password.text()


    def _reset(self):
        self.username._reset()
        self.password._reset()



