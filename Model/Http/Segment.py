import asyncio
import time, os

import httpx as hx

from Model.Util import compare_file_url

from Utility.Core import STATUS, STATES, DATA_UNIT, HTTP
from Utility.URL import request_header


class Segment:

    def __init__(self, url, file_path, start, length, etag):
        self.url = url
        self.file_path = file_path
        self.start = start
        self.length = length
        self.etag = etag

        self.pause = True
        self.state = STATES.PAUSED
        self.status = STATUS.PAUSED

        self.__running = False
        self.__allowed = False

        self.ping = 0
        self.downloaded = 0
        self.max_duration = 1

        self.buffer = asyncio.Queue()

        self.__check_downloaded()



    async def put_to_buffer(self, chunk):
        self.downloaded += len(chunk)
        await self.buffer.put(chunk)
    

    # fetch url data from network
    async def fetch(self, client):
        
        while not self.is_completed() and not self.is_paused():

            if not self.__allowed:
                self.set_status(STATUS.PENDING)
                await asyncio.sleep(0.25)
                continue

            self.set_status(STATUS.CONNECTING)

            try:
                header = self.__make_header()
                async with client.stream('GET', self.url, headers = header) as stream:
                    
                    if stream.is_error:
                        await self.__check_error(stream)
                        break

                    self.__set_running(True)
                    self.set_status(STATUS.DOWNLOADING)

                    start_time = time.time()
                    ping_time = time.time()

                    self.set_status(STATUS.DOWNLOADING)

                    async for chunk in stream.aiter_bytes():

                        self.ping = time.time() - ping_time
                        ping_time = time.time()

                        await self.put_to_buffer(chunk)

                        # if specified time passed then write fetched data into the file
                        if (time.time() - start_time) >= self.max_duration:
                            await self.write_buffer()
                            start_time = time.time()

                            self.set_status(STATUS.DOWNLOADING)

                        if self.is_paused() or not self.__allowed:
                            break
                    
                    # write for last time for sure
                    await self.write_buffer()

            except hx.ConnectError:
                self.set_status(STATUS.CONNECT_ERROR)
                break

            # in case of connect timeout we must retry again
            # but for now lets stop it here, maybe in future updates...
            except hx.ConnectTimeout:
                self.set_status(STATUS.CONNECT_ERROR)
                break

            except hx.ReadTimeout:
                self.set_status(STATUS.TIMEOUT_ERROR)
                
            
            except Exception as e:
                print(type(e), e)
            
            finally:
                await self.write_buffer()
        


    def __set_running(self, state):
        self.__running = state
    
    def is_running(self):
        return self.__running

    def is_allowed(self):
        return self.__allowed
    
    def set_allowed(self, state):
        self.__allowed = state

    def get_ping(self):
        return self.ping
    

    async def __check_error(self, response):
        
        status = HTTP.RESPONSE.ERROR_STATUS.get(response.status_code)
        self.set_status(status)



    async def run(self, client):
        await self.__check_file()
        await self.fetch(client)
        
        self.set_pause(True)
        self.__set_running(False)



    def get_downloaded(self):
        return self.downloaded


    def is_completed(self):
        return self.downloaded == self.length


    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state


    def get_status(self):
        return self.status

    def set_status(self, status):
        if status != self.get_status():
            self.status = status


    def is_paused(self):
        return self.pause

    def set_pause(self, pause):

        self.pause = pause

        state = STATES.PAUSED
        status = STATUS.PAUSED

        if not pause:
            if self.is_completed():
                state = STATES.COMPLETED
                status = STATUS.COMPLETED
            else:
                state = STATES.RUNNING
                status = STATUS.CONNECTING
        
        if not self.get_status().is_error():
            self.set_status(status)
            
        self.set_state(state)
    

    def __check_downloaded(self):
        if os.path.exists(self.file_path):
            self.downloaded = os.lstat(self.file_path).st_size


    # check file if data in it is correct or corrupted
    async def __check_file(self):

        self.set_status(STATUS.CHECKING)
        
        if os.path.exists(self.file_path) and self.downloaded > (32 * DATA_UNIT.KB):
        
            is_same = await compare_file_url(self.url, self.file_path, self.start, self.downloaded)

            if not is_same:
                self.downloaded = 0
                with open(self.file_path, 'w') as _:
                    pass



    async def write_buffer(self):
        
        count = 0
        max_opt = 30

        if self.buffer.empty():
            return
        
        self.set_status(STATUS.WRITING)

        with open(self.file_path, 'ab') as file:

            while not self.buffer.empty():
        
                chunk = await self.buffer.get()
                file.write(chunk)

                count += 1

                if count > max_opt:
                    await asyncio.sleep(0.08)
                    count = 0

    
    # make conditional header for get request
    def __make_header(self):
        
        start = self.start + self.downloaded
        stop = self.start + self.length - 1
        etag = self.etag
        date = None

        return request_header(start, stop, etag, date)



    def __repr__(self):
        return self.file_path
    
    def __str__(self):
        return f'{self.file_path} -- {self.start} -- {self.length} -- {self.downloaded}'
    



