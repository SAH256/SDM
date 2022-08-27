import asyncio, shutil, time, os
import httpx as hx

from Model.Util import get_url_info

from Utility.Structure.Task.Base import Request
from Utility.Util import write_to_file, create_segment_name
from Utility.Actions import remove_file, remove_dir
from Utility.Core import STATUS, DATA_UNIT

from .Segment import Segment


class Manager:

    def __init__(self, url, file_name, size, part, temp_path, save_path, etag):
        self.url = url
        self.file_name = file_name
        self.size = size
        self.part = part
        self.etag = etag

        self.temp_path = temp_path
        self.save_path = save_path
        
        self.segments = []

        self.start_time = None
        self.downloaded = 0
        self.speed = 0
        self.progress = 0
        self.paused = True
        self.status = None

        self.max_active = (part // 4) + 1


        self.__fetch_completed = False
        self.__build_completed = False
        self.__joining = False

        self.setting = {
            'timeout' : hx.Timeout(10, connect = 30, read = 15)
        }
    

    def __create_segments(self):

        part_share = self.size // self.part
        length, start = None, None

        for counter in range(self.part):
            
            start = counter * part_share

            if counter < (self.part - 1):
                length = part_share
            else:
                length = self.size - start

            segment_name = create_segment_name(counter + 1)
            file_path = os.path.join(self.temp_path, segment_name)
            
            new_segment = Segment(self.url, file_path, start, length, self.etag)

            self.segments.append(new_segment)


    def pause(self):
        self.paused = True
        self.__set_segment_pause(self.paused)

    def resume(self):
        self.paused = False
        self.__set_segment_pause(self.paused)


    def __set_segment_pause(self, state):
        for item in self.segments:
            item.set_pause(state)


    def is_paused(self):
        return self.paused

    def is_completed(self):
        return self.__fetch_completed and self.__build_completed

    def is_joining(self):
        return self.__joining
    
    def __set_joining(self, state):
        self.__joining = state


    async def __check_segment_download(self):
        state = True

        for segment in self.segments:
            if not segment.is_completed() and segment.is_running():
                state = False
                break
                
        self.__fetch_completed = state and (self.downloaded == self.size)


    
    async def download_segments(self):

        async with hx.AsyncClient(http2 = True, **self.setting) as client:
            self.set_status(STATUS.CONNECTING)

            coroutines = []

            for segment in self.segments:
                segment.set_pause(False)
                coroutines.append(segment.run(client))

            await asyncio.gather(*coroutines)


    # manage segments and run one by one
    # run first one if there is no error run next one
    # meanwhile check other criteria
    async def manage_segments(self):
        
        while not self.__fetch_completed and not self.is_paused():

            running_count = await self.__get_active_count()

            for index, segment in enumerate(self.segments):                
                if segment.is_running() or segment.is_completed():
                    continue

                if index:
                    
                    if running_count < self.max_active or self.get_ping() < 0.25:
                        prev_segment = self.segments[index - 1]

                        if prev_segment.is_running() or prev_segment.is_completed():
                            segment.set_allowed(True)
                            await asyncio.sleep(0.1)
                            running_count += 1
                else:
                    if not segment.is_allowed() and not segment.is_completed():
                        segment.set_allowed(True)
                    else:
                        status = segment.get_status()
                        
                        if status.is_error():
                            self.set_status(status)
                            self.pause()
                            break
                            
            # check temp save path's disk usage
            if shutil.disk_usage(self.temp_path).free <= (300 * DATA_UNIT.MB):
                self.set_status(STATUS.LOW_STORAGE_ERROR)
                self.pause()
                
            await asyncio.sleep(0.25)


    # find avg of segments' pings
    # this function may need some revisions
    def get_ping(self):

        total = 0
        count = 0
        ping = 9999

        for segment in self.segments:
            if segment.is_running():
                total += segment.get_ping()
                count += 1

        if count:
            ping = round(total / count, 4)

        return ping


    async def check_segments(self):
        
        start_time = time.time() + 0.1
        sleep_time = 0.45
        last_down = self.__sum_segments_download()
        last_speeds = [0] * 4
        index = 0

        while not self.__fetch_completed and not self.is_paused():

            downloaded = self.__sum_segments_download()
            duration = time.time() - start_time

            if downloaded > 0:
                self.set_status(STATUS.DOWNLOADING)

            temp = (downloaded - last_down) / duration
            last_speeds[index] = temp
            index += 1

            if index >= len(last_speeds):
                index = 0
            
            speed = sum(last_speeds) / len(last_speeds)   #change to bits for speed


            self.speed = round(speed, 2)
            self.downloaded = downloaded
            self.progress = round(downloaded / self.size, 4)

            start_time = time.time()
            last_down = downloaded

            await self.__check_segment_download()
            await asyncio.sleep(sleep_time)


    # starting point of running manager's async functions
    async def fetch_data(self):

        self.__create_segments()

        # create tasks from concurrent functions
        download_task = asyncio.create_task(self.download_segments())
        manage_task = asyncio.create_task(self.manage_segments())
        check_task = asyncio.create_task(self.check_segments())

        await download_task
        await manage_task
        await check_task
        await self.__join_segments()
        await self.__check_segments_status()


    # final checking of segments in case of error and unintended pause
    async def __check_segments_status(self):
        all_status = []

        for segment in self.segments:
            status = segment.get_status()

            if status and status.is_error():
                all_status.append(status)
        
        if all_status:
            self.set_status(all_status[0])


    # join segments temp files and create actual file
    async def __join_segments(self):

        if not self.__fetch_completed:
            return

        if shutil.disk_usage(self.save_path).free < self.size:
            self.status = STATUS.LOW_STORAGE_ERROR
            return

        self.__set_joining(True)

        self.progress = 0

        path_iter = os.scandir(self.temp_path)
        save_dir = os.path.join(self.save_path, self.file_name)

        total_size = 0
        stop_write = False


        for index, entry in enumerate(path_iter):

            gen = write_to_file(save_dir, entry.path, append = (index != 0))
            async_counter = 0

            for size in gen:
                if size < 0:
                    stop_write = True
                    break

                total_size += size
                self.progress = round(total_size / self.size, 4)
                async_counter += 1

                if async_counter > 50:
                    async_counter = 0

                    await asyncio.sleep(0.2)
                    time.sleep(0.05)
            
                if self.is_paused():
                    stop_write = True
                    self.progress = 1
                    del gen
                    break
            
            if stop_write:
                break


            time.sleep(0.3)

        
        if stop_write:
            # remove uncompleted file
            remove_file(save_dir)
        else:
            # remove temp folder and files
            remove_dir(self.temp_path)
            self.__build_completed = True

        self.__set_joining(False)


    async def __get_active_count(self):
        count = 0

        for segment in self.segments:
            if segment.is_running():
                count += 1
        
        return count


    def __sum_segments_download(self):
        downloaded = 0

        for segment in self.segments:
            downloaded += segment.get_downloaded()
        
        return downloaded


    def get_speed(self):
        return self.speed


    # if manger is running, manage_segments function will update downloaded
    # else we update it ourselves
    def get_downloaded(self):
        if not self.is_paused():
            return self.downloaded
        else:
            return self.__sum_segments_download()
    
    def get_progress(self):
        return self.progress

    def get_eta(self):
        eta = -1
        remain = self.size - self.downloaded

        eta = round(remain / (self.speed + 10))
        
        return eta

    def get_status(self):
        return self.status

    def set_status(self, status):
        if self.get_status() != status:
            self.status = status
