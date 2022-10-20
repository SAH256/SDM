import sys, time
import _config

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QSharedMemory

from Model.Client import Client

from UI.Main.Window.MainWindow import MainWindow

from Utility.Structure.Setting import Setting
from Utility.Actions import check_essential_folders
from Utility.Core import PLATFORMS


# Start point of program
class Application(QApplication):

    def __init__(self, key):
        super().__init__([])

        self.__running = False
        self.__user_exit = False
        
        if sys.platform != PLATFORMS.WINDOWS:
            QSharedMemory(key).attach()
        
        self._memory = QSharedMemory(self)
        self._memory.setKey(key)
        
        if self._memory.attach():
            self.__running = True
            
        elif not self._memory.create(1):
            raise RuntimeError(self._memory.errorString())
    
    
    def is_running(self):
        return self.__running


    def setup(self):
        self.__setup_model()
        self.__setup_ui()
        self.__perform_checks()
    

    def __setup_model(self):
        self.setting = Setting()
        setting = self.setting.get_client_setting()

        self.client = Client(setting)
        self.client.restore_state()


    def __setup_ui(self):
        self.ui = MainWindow(self.client, self.setting)
        self.ui.setup()
        self.ui.user_exited.connect(self.__exit_handler)

        style = self.setting.get_interface().get_current_stylesheet()
        self.ui.setStyleSheet(style)


    def __exit_handler(self):
        self.__user_exit = True


    def __perform_checks(self):
        check_essential_folders()

    
    def exec(self):
        while not self.__user_exit:
            # change Interface options

            self.ui.show()
            super().exec()
            time.sleep(1)

            self.client.save_state()
            self.setting.save_setting()

        self.client.stop_session()
        time.sleep(2)
        
        return 0



if __name__ == '__main__':
    key = 'SDM'
    
    try:
        app = Application(key)
        
        if app.is_running():
            title = 'Program is running'
            txt = 'A Program Instance is still running....'
            QtWidgets.QMessageBox.warning(None, title, txt)
        else:
            app.setup()
            sys.exit(app.exec())
        
    except RuntimeError as e:
        print(e)

