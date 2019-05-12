
import time
import datetime
# from collections import Iterable, Iterator
times = '14:00'
times = datetime.datetime.strptime(times, '%H:%M')

print(times.time())
date = '2012-05-08'
date = datetime.datetime.strptime(date, '%Y-%m-%d')
print(date + datetime.timedelta(hours=times.hour)) #组合时间

#测试使用迭代器生成日期
# def datellist(start_date, end_date):
#     # datelist = []
#     if start_date < end_date:
#         raise 'start_date biger than end_date'
#     date = start_date
#     while date <= end_date:
#         # datelist.append(date)
#         yield date
#         date = date + datetime.timedelta(days=1)
#
#
# start_date = datetime.datetime.strptime('2012-05-08', '%Y-%m-%d')
# end_date = datetime.datetime.strptime('2012-05-10', '%Y-%m-%d')
# datelist = datellist(start_date, end_date)
# print(next(datelist))
# for i in datelist:
#     print(i)

# print(next(datelist))
# print(next(datelist))
# print(isinstance(datelist, Iterable))
# # print(len(datelist))
# print(next(datelist))


time = [{ 'start_date': '2012-05-08', 'end_date': '2012-05-10', 'start_time': '14:00', 'end_time': '16:00' }]
def date_iterator(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    if start_date > end_date:
        raise Exception('start_date bigger than end_date')
    date = start_date
    while date <= end_date:
        yield date
        date = date + datetime.timedelta(days=1)
#存放每一个时间段里面的迭代器对象
list_date_iterator = []
for i in time:
    date = date_iterator(i['start_date'], i['end_date'])
    list_date_iterator.append(date)
    print('123',next(date))
    for s in date:
        print(s)
    # for s in date:
    #     print(s)

# 寻找最小时间作为项目开始时间， 最大时间作为项目结束时间
def get_start_end(timetable):
    min_datetime = datetime.datetime.strptime(timetable[0]['start_date']+' '+timetable[0]['start_time'], '%Y-%m-%d %H:%M')
    max_datetime = datetime.datetime.strptime(timetable[0]['end_date']+' '+timetable[0]['end_time'], '%Y-%m-%d %H:%M')
    for i in timetable:
        start = datetime.datetime.strptime(i['start_date'] + ' ' + i['start_time'], '%Y-%m-%d %H:%M')
        end = datetime.datetime.strptime(i['end_date'] + ' ' + i['end_time'], '%Y-%m-%d %H:%M')
        if start < min_datetime:
            min_datetime = start
        if end > max_datetime:
            max_datetime = end
    return (min_datetime, max_datetime)
# print(max_datetime, min_datetime)