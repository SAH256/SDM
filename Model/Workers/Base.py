from PyQt5.QtCore import QObject, pyqtSignal



class BaseWorker(QObject):
    finished = pyqtSignal()



class TaskWorker(BaseWorker):
    fetched = pyqtSignal(list)
    finished = pyqtSignal(str)






