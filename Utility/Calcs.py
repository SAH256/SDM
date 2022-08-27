import datetime as dt

from .Core import WEEK, PATTERNS


# get local date-time object
def get_local():
    return dt.datetime.now()
    


def create_td(time_object):
    return dt.timedelta(hours = time_object.hour, minutes = time_object.minute, seconds = time_object.second)


def difference_time(checkpoint):

    local = get_local().time()

    now = create_td(local)
    check = create_td(checkpoint)

    result = check - now

    return result.seconds * 1000


# find how much microseconds is remain until midnight
def until_midnight():
    now = dt.datetime.now()
    mid = now.replace(hour = 23, minute = 59, second = 59, microsecond = 999)

    result = mid - now

    return result.seconds * 1000


def get_today_week(index = True):

    day = dt.datetime.now().isoweekday()

    if index:
        return day

    return WEEK.index_to_day[str(day)]


def get_today():
    return get_local().date()


def is_today(date, time):
    r = False

    if date == get_today():
        now = get_local()
        mid = dt.time(23, 59, 59)
        mid = mix_date_time(now, mid)

        req = mix_date_time(date, time)


        if now <= req <= mid:
            r = True

    return r


def mix_date_time(date, time):
    return dt.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second)


def change_to_micro(time_tuple):
    total = 0
    
    total += time_tuple[0] * 3600
    total += time_tuple[1] * 60

    return total * 1000




def time_passed(time):
    now = get_local()
    req = mix_date_time(now.date(), time)

    return now >= req



def format_timestamp(tm):
    if tm <= 0:
        return ''

    new_date = dt.datetime.fromtimestamp(tm)
    return new_date.strftime(PATTERNS.POSIX_PATTERN)


def format_remain_time(tm):
    s = tm
    m = None
    h = None
    d = None

    if s >= 60:
        m = s // 60
        s %= 60
    
    if m and m >= 60:
        h = m // 60
        m %= 60
    
    if h and h >= 24:
        d = h // 24
        h %= 25
    
    keys = [(s, 'sec'), (m, 'm'), (h, 'h'), (d, 'd')]

    result = ''

    for value, suf in keys:
        if value:
            result = f" {value} {suf}" + result
        else:
            break
        
    
    return result
