import datetime
import time
from datetime import datetime as Datetime
from datetime import timedelta

import beni.http as bhttp

_DEFAULT_FMT = '%Y-%m-%d %H:%M:%S'


def timestamp_bystr(value: str, fmt: str = _DEFAULT_FMT):
    return time.mktime(time.strptime(value, fmt))


def timestamp_tostr(timestamp: float | None, fmt: str = _DEFAULT_FMT):
    timestamp = timestamp or time.time()
    ary = time.localtime(timestamp)
    return time.strftime(fmt, ary)


def date(date_str: str, fmt: str = '%Y-%m-%d'):
    return datetime.datetime.strptime(date_str, fmt).date()


async def network_time():
    _, response = await bhttp.get('https://www.baidu.com')
    date_str = response.headers['Date']
    datetime = Datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT') + timedelta(hours=8)
    return datetime
