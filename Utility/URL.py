from urllib.parse import unquote_plus
import datetime as dt
import re

from .Core import TORRENT, HTTP, PATTERNS, LINK_TYPE


# make get header request
def request_header(start, stop, etag = None, date = None):

    header = {HTTP.HEADER.RANGE : f'bytes={start}-{stop}'}

    if etag:
        header[HTTP.HEADER.IF_MATCH] = etag
    
    if date:
        header[HTTP.HEADER.IF_UNMODIFIED] = date

    return header


# file file name from url
def find_filename(url):
    result = re.search(PATTERNS.FILE_NAME_PATTERN, url)
    if result is not None:
        result = result.group(0)
    else:
        result = url.split("/")[-1]
    
    return unquote_plus(result)


# find url type from context
def url_type(url):
    t = None

    if url.startswith(HTTP.PROTOCOL.HTTP) or url.startswith(HTTP.PROTOCOL.FTP):
        t = LINK_TYPE.HTTP
    elif url.startswith(TORRENT.MAGNET_TAG) or url.endswith(TORRENT.TORRENT_EXT):
        t = LINK_TYPE.MAGNET
    
    return t


# find magnet type from text provided
def magnet_type(text):
    
    if text.startswith(TORRENT.MAGNET_TAG):
        return TORRENT.MAGNET_LINK
    elif text.endswith(TORRENT.TORRENT_EXT):
        return TORRENT.TORRENT_FILE


def remove_quote(item):
    return item.replace('"', '').replace("'", "")


# split multi values header data
def split_headers(header_option):
    res = {}
    for index, item in enumerate(header_option.split("; ")):
        if item.count("="):
            item = item.split("=")
            res[item[0]] = remove_quote(item[1])
        else:
            res[index] = item
    return res


# set url_info object data from header object
def header_handler(header, url_info):

    if HTTP.TYPE.HTML in header.get(HTTP.HEADER.CONTENT_TYPE):
        url_info.code = HTTP.RESPONSE.WEBPAGE_RECIEVED
        return


    _range = header.get(HTTP.HEADER.SUPPORTED_RANGE)
    if _range and _range != HTTP.HEADER.NONE:
        url_info.resume = True

                
    dispos = header.get(HTTP.HEADER.DISPOSITION, None)

    if dispos:
        temp = split_headers(dispos)
        url_info.name = temp.get(HTTP.HEADER.FILE_NAME, None)
        
    
    if not url_info.name:
        url_info.name = find_filename(url_info.url)
                    

    length = header.get(HTTP.HEADER.CONTENT_LENGTH, 0)
    url_info.size = int(length)
    url_info.etag = header.get(HTTP.HEADER.ETAG)
    url_info.date = header.get(HTTP.HEADER.LAST_MODIFIED)
