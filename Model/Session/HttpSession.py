from PyQt5 import QtCore

from Model.Http.Session import Session
from Model.Workers.Session.Http import HttpSessionWorker

from Utility.Core import STATES, STATUS

from .BaseSession import BaseSession



class HttpSession(BaseSession):
    
    def __init__(self, setting = None):
        super().__init__(setting)
        self.session = Session()
    
    def add_task(self, task, data = None):
        super().add_task(task)
        self.session.add_task(task)


    def pause_task(self, request):
        task = self.__get_task(request.get_id())

        if task:
            task.set_status(STATUS.PAUSED)
            self.session.pause_task(request.get_id())
            

    def resume_task(self, request):
        task = self.__get_task(request.get_id())

        if task:
            task.set_status(STATUS.CONNECTING)
            self.session.resume_task(request.get_id())


    def remove_task(self, request):
        task = self.tasks.pop(request.get_id(), None)

        self.session.remove_task(request.get_id())
    
    def __get_task(self, _id):
        return self.tasks.get(_id)

    def pause(self):
        super().pause()
        self.session.stop()


    # if session isn't running then start thread
    def resume(self):

        if not self.running:
            
            self.__start_worker()

        super().resume()
    
    def __start_worker(self):
        
        self.thread = QtCore.QThread()
        self.worker = HttpSessionWorker(self.session)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.__release_thread)

        self.thread.start()
    

    def __release_thread(self):
        self.running = False





















