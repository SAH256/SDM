import uuid as uid
import os

from .Core import DATA_UNIT, PATTERNS, LINK_TYPE

# read or write from file
def file_ops(file_name, data = None, read = True, binary = True):

    mode = ('r' if read else 'w')
    
    if binary:
        mode += 'b'

    with open(file_name, mode) as file:
        if read:
            data = file.read()
        else:
            file.write(data)

    if read:
        return data
    else:
        return None


# change size to string unit
def sizeChanger(size):
    prefix = DATA_UNIT.BYTE

    if size <= 0:
        return f'{size} {DATA_UNIT.UNITS[prefix]}'

    for unit in DATA_UNIT.UNITS:
        if size >= unit:
            prefix = unit

    value = round(size / prefix, 2)
    
    return f'{value:.2f} {DATA_UNIT.UNITS[prefix]}'


def create_id(url, name = None, time_stamp = None):

    d = uid.uuid3(uid.NAMESPACE_URL, url)

    if name:
        d = uid.uuid3(d, name)

    if time_stamp:
        d = uid.uuid5(d, str(time_stamp))

    return d.hex


def create_segment_name(number):
    return f'TEMP_FILE_{str(number).zfill(2)}'
      

# split filename to name and extension
def split_file_name(file_name):
    split = os.path.splitext(file_name)
    data = split[0], split[1][1:]           # removing the '.' in extension

    return data


def add_file_number(file_name, number):
    name, ext = split_file_name(file_name)

    print(name, ext)

    return f'{name}_{number}.{ext}'


def write_to_file(dest_path, source_path, append = False):
    CHUNK_SIZE = 512 * DATA_UNIT.KB
    mode = 'wb'

    if not os.path.exists(source_path):
        return -1
    
    if append:
        mode = 'ab'
    
    with open(dest_path, mode) as dest, open(source_path, mode = 'rb') as source:
        is_ok = True

        while is_ok:

            chunk = source.read(CHUNK_SIZE)

            if chunk:
                dest.write(chunk)
                yield len(chunk)
            else:
                is_ok = False


# find appropriate default part count based on size and resumability
def get_default_part(size, resume = False):
    part = 1

    if resume:
        if size <= (10 * DATA_UNIT.MB):
            part = int(size // (2.5 * DATA_UNIT.MB)) + 1
        else:
            part = 10

    return part






