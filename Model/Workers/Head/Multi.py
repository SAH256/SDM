import asyncio
import httpx as hx

from Utility.Structure.Task.Http import HttpMetadata
from Utility.URL import header_handler
from Utility.Core import HTTP

from ..Base import TaskWorker


class MultiWorker(TaskWorker):

    def __init__(self, request):
        super().__init__()

        self.request = request
        self.loop = asyncio.new_event_loop()
        self.sem = asyncio.Semaphore(10, loop = self.loop)


    async def request_handler(self, client, req):

        async with self.sem:            
            info = HttpMetadata(req.get_id(), req.url)
            state = False

            try:
                res = await client.head(req.url, auth = (req.user, req.password))

                info.url = str(res.url)
                info.code = res.status_code

                header_handler(res.headers, info)
        
            except hx.ConnectError:
                info.code = HTTP.RESPONSE.CONNECT_ERROR

            except hx.ConnectTimeout:
                info.code = HTTP.RESPONSE.CONNECT_ERROR
            
            except Exception as e:
                pass

            self.fetched.emit( [self.request.get_id(), (req.get_id(), info)] )


    async def __create_tasks(self):
        t = 60

        async with hx.AsyncClient(timeout = t, follow_redirects = True, http2 = True) as client:
            tasks = []

            for req in self.request.link_iter:
                task = asyncio.create_task(self.request_handler(client, req))
                tasks.append(task)
                
            await asyncio.gather(*tasks, loop = self.loop)


    def run(self):

        self.loop.run_until_complete(self.__create_tasks())
            
        self.finished.emit(self.request.get_id())













