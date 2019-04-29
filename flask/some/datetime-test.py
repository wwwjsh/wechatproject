import datetime
# d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
# d2 = datetime.datetime.strptime('2012-03-02 17:40:20', '%Y-%m-%d %H:%M:%S')
# delta = d1 - d2

start_time = "2012-1-1 14:00"
end_time = "2012-1-1 16:00"
timelist = []
minOrd_time = 60
# print(start_time<end_time)
# print(str(start_time))
def divi_stime(start_time,end_time):
    start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
    time = start
    while time < end:
        timelist.append(str(time))
        time = time + datetime.timedelta(minutes=minOrd_time)
    print(timelist)
divi_stime(start_time,end_time)
