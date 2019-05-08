import datetime
# d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
# d2 = datetime.datetime.strptime('2012-03-02 17:40:20', '%Y-%m-%d %H:%M:%S')
# delta = d1 - d2
import json
start_time = "2012-1-1 14:00"
end_time = "2012-1-1 16:00"
time3 = "2019-05-05 14:00"
timelist = []
minOrd_time = 60
# print(start_time<end_time)
# print(str(start_time))
time1 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
time2 = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
time3 = datetime.datetime.strptime(time3, '%Y-%m-%d %H:%M')

def divi_stime(start_time,end_time):
    start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
    time = start
    while time < end:
        timelist.append(str(time))
        time = time + datetime.timedelta(minutes=minOrd_time)
    print(timelist)
# divi_stime(start_time,end_time)
print(time2.year) # 年
# obj_data = [{'start_time': time1, 'obj':[123]}, {'start_time': time2, 'obj': [1,5,6]}]
obj_data = [{'start_time': time1, 'obj': [{'obj_id': 179, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 182, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}, {'start_time': time2, 'obj': [{'obj_id': 180, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 183, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}, {'start_time': time3, 'obj': [{'obj_id': 181, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 184, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}]

print(obj_data)
#截取时间列表
date_list = []
dealed_data = []
for  data in obj_data:
    date = [data['start_time'].year, data['start_time'].month, data['start_time'].day]
    data['start_time'] = [data['start_time'].hour, data['start_time'].minute] # 修改开始时间格式
    # print(date) # 返回日期列表
    if date not in date_list:
        date_list.append(date)
        dealed_data.append({'date':date, 'objs':[data]})
    else:
        for i in range(len(dealed_data)):
            if dealed_data[i].get('date', 0) == date:
                dealed_data[i]['objs'].append(data)


print(dealed_data)
print(len(dealed_data))
print(time2.date()==time1.date())
# def equal_date(tiem1, tiem2):
