# 生成当前时间的时间戳，只有一个参数即时间戳的位数，默认为10位，输入位数即生成相应位数的时间戳，比如可以生成常用的13位时间戳
import math
import time

from common.LogUtil import LogUtil


def now_to_timestamp(digits=10):
    time_stamp = time.time()
    digits = 10 ** (digits - 10)
    time_stamp = int(round(time_stamp * digits))
    return time_stamp


# 将时间戳规范为10位时间戳
def timestamp_to_timestamp10(time_stamp):
    time_stamp = int(time_stamp * (10 ** (10 - len(str(time_stamp)))))
    return time_stamp


# 将当前时间转换为时间字符串，默认为2017-10-01 13:37:04格式
def now_to_date(format_string="%Y-%m-%d %H:%M:%S"):
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


# 将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


# 将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def get_time():
    from time import time
    now = int(1000 * time())
    return str(now)


def get_time_after(wait_time):
    from time import time
    now = int(1000 * (time() + wait_time))
    return str(now)


# 将传入的ISO8601 时间字符串，转成成指定格式的Local时区字(UTC+8)符串
def isoStr2utc8Str(isoStr):
    # 取出timestamp，解析转成iso8601 navie datetime
    from datetime import datetime
    utc = datetime.strptime(isoStr, '%Y-%m-%dT%H:%M:%S.%fZ')
    # utc navie datetime设置时区，再换成本地时区，最后解析成字符串。时区可以硬编码。
    from dateutil.tz import tz
    utc8Time = utc.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()).strftime(
        '%Y-%m-%d %H:%M:%S.%f')[:-3]
    # utc8Time = utc.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()).replace(tzinfo=None)
    return utc8Time


# 不同时间格式字符串的转换
def date_style_transfomation(date, format_string1="%Y-%m-%d %H:%M:%S",
                             format_string2="%Y-%m-%d %H-%M-%S"):
    time_array = time.strptime(date, format_string1)
    str_date = time.strftime(format_string2, time_array)
    return str_date


def change_to_formattime(allTime):
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if allTime < 60:
        return "%d秒" % math.ceil(allTime)
    elif allTime > day:
        days = divmod(allTime, day)
        return "%d天%s" % (int(days[0]), change_to_formattime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime, hour)
        return '%d小时%s' % (int(hours[0]), change_to_formattime(hours[1]))
    else:
        mins = divmod(allTime, min)
        return "%d分钟%d秒" % (int(mins[0]), math.ceil(mins[1]))


# "time": "2020-01-18 09:58:35.616",
# "@timestamp": "2020-01-18T01:58:36.224Z",
if __name__ == '__main__':
    time_stamp = str(int(now_to_timestamp(8)))
    LogUtil.info(now_to_date() + "对应的时间戳==>" + time_stamp)
    timestamp = date_to_timestamp('2020-01-18T01:58:36.224Z', "%Y-%m-%dT%H:%M:%S.%fZ")
    LogUtil.info(timestamp_to_date(timestamp))
    timestamp = date_to_timestamp('2020-01-18 09:58:35.616', "%Y-%m-%d %H:%M:%S.%f")
    LogUtil.info(timestamp_to_date(timestamp))
