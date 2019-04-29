import requests
import json
url = "http://127.0.0.1:5000/joinAcitvity"
url2 = "http://127.0.0.1:5000/joinInfo?wd=hg7v0"
openid = 123456
ord_price = 0
objId = [2,3]
# hg7v0

# #ord_objects: [{obj_num: int(3), obj_name: varchar(15), minOrd_time: time, ordable_sum: int(3)}]}
data = {
"ord_usId" : json.dumps(openid),
"ord_price" : json.dumps(ord_price),
"objId" :  json.dumps(objId),
}
header = {
            'content-type': 'application/x-www-form-urlencoded',
            'chartset': 'utf-8'
          }


data2 = {"wd": "hg7v0"}

session = requests.Session()
session.headers = header

responses = session.get(url = url2)
responses.encoding = 'utf-8'
print(responses.text)