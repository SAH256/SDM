from ..Base import BaseWorker


# Simple Http worker class
class HttpSessionWorker(BaseWorker):

    def __init__(self, session):
        super().__init__()

        self.session = session


    def run(self):
        self.session.start()

        self.finished.emit()












