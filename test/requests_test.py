import requests
import json
url = "http://127.0.0.1:5000/launchActivity"
openid = "123456"
token = '7376b0ce15ca4502dd626cf16852c8f6'
item_name = "天玄"
item_type = "1"
contacts = "1354852"
start_time = "2012-1-1 14:00"
end_time = "2012-1-1 17:00"
item_address = "广州"
text_info = "记得来"
ord_objects = [{"obj_num": 1, "obj_name": "一号桌", "minOrd_time": 60, "ordable_sum": "30"}]
# #ord_objects: [{obj_num: int(3), obj_name: varchar(15), minOrd_time: time, ordable_sum: int(3)}]}
data = {
"token" : json.dumps(token),
"item_name" : json.dumps(item_name),
"item_type" :  json.dumps(item_type),
"contacts" :  json.dumps(contacts),
"start_time" :  json.dumps(start_time),
"end_time" : json.dumps(end_time),
"item_address" : json.dumps(item_address),
"text_info" : json.dumps(text_info),
"ord_objects" : json.dumps(ord_objects),
}
header = {
            'content-type': 'application/x-www-form-urlencoded',
            'chartset': 'utf-8'
          }



session = requests.Session()
session.headers = header

responses = session.post(url = url, data = data)
responses.encoding = 'utf-8'
print(responses.text)
# session.mount("http://127.0.0.1", SourcePortAdapter(54321))