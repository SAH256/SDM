import asyncio
import httpx as hx

from Utility.Core import HTTP, DATA_UNIT

from Utility.Structure.Task.Http import HttpMetadata
from Utility.URL import header_handler, request_header



# HEAD request
async def get_url_info(req):

    t = 60
    auth = None
    info = HttpMetadata(req.get_id(), req.url)

    if req.has_auth():
        auth = req.user, req.password

    try:
        async with hx.AsyncClient(timeout = t, follow_redirects = True, auth = auth) as client:
            
            res = await client.head(req.url)
            
            info.url = str(res.url)
            info.code = res.status_code

            header_handler(res.headers, info)
    
    except Exception as e:
        info.code = HTTP.RESPONSE.CONNECT_ERROR

    return info



# GET request with limited range
async def get_url_data(url, start, length):

    header = request_header(start, start + length - 1)

    data = b''

    try:
        async with hx.AsyncClient(timeout = 30, follow_redirects = True) as client:

            res = await client.get(url, headers = header, timeout = 30)

            data = res.read()

    except Exception as e:
        data = None

    return data


# function for copying a file data
async def get_file_data(file_name, start, length):

    data = b''

    with open(file_name, 'rb') as file:
        file.seek(start)
        data = file.read(length)
    
    return data



# comparing file data with a url data based on position and size
async def compare_file_url(url, file_name, url_start, file_size):
    offset = 100

    if file_size > DATA_UNIT.MB:
        offset = 32 * DATA_UNIT.KB
        
    req_ranges = [
        [(url_start, offset), (0, offset)],
        [(url_start + file_size - offset, offset), (file_size - offset, offset)]
    ]

    result = True

    for url_range, file_range in req_ranges:

        task_1 = asyncio.create_task(get_url_data(url, *url_range))
        task_2 = asyncio.create_task(get_file_data(file_name, *file_range))

        url_data = await task_1
        file_data = await task_2

        if url_data == None:
            return

        result = result and (url_data == file_data)

    return result



# this is for running async manager obj in thread
def run_task(manager):

    asyncio.run(manager.fetch_data())



