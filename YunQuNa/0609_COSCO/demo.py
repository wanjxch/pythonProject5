import time, re

# 获取当前时间的本地时间，以结构化的方式表示
currenttime = time.localtime()
print('currenttime: ', currenttime)   # 时间对象

current_time = time.strftime("%Y-%m-%d %H:%M:%S", currenttime) # 转化为字符串
print('current_time: ', current_time)

time_obj = time.strptime(current_time, "%Y-%m-%d %H:%M:%S")  # 转化为时间对象
print('time_obj: ', time_obj)

time_stamp = time.mktime(time_obj)
print('time_stamp: ', time_stamp)        # 时间戳 （1687950111.0） , 10位


def date_to_format_data(orign_datetime_string):
    """ 2018-11-03 22:24 转化为 2018-11-03 22:24:00 """
    if orign_datetime_string:
        datetime_string = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', orign_datetime_string)
        struct_time = time.strptime(datetime_string[0], '%Y-%m-%d %H:%M')
        datetime_string = time.strftime('%Y-%m-%d %H:%M:%S', struct_time)
        return datetime_string  #

# print(date_to_format_data("2018-11-03 22:24"))
