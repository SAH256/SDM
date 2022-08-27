import asyncio

from Model.Util import get_url_info
from Utility.Core import HTTP

from ..Base import TaskWorker


class SingleWorker(TaskWorker):

    def __init__(self, req):
        super().__init__()
        
        self.req = req
    

    def run(self):

        metadata = None
        state = False

        metadata = asyncio.run(get_url_info(self.req))

        self.fetched.emit([self.req.get_id(), metadata])

        self.finished.emit(self.req.get_id())


