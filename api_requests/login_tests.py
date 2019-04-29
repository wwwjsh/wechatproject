import requests
import json
url = "http://127.0.0.1:5000/joinAcitvity"
url2 = "http://127.0.0.1:5000/userinfo"
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


data2 = {'encryptedData': json.dumps('CiyLU1Aw2KjvrjMdj8YKliAjtP4gsMZMQmRzooG2xrDcvSnxIMXFufNstNGTyaGS9uT5geRa0W4oTOb1WT7fJlAC+oNPdbB+3hVbJSRgv+4lGOETKUQz6OYStslQ142dNCuabNPGBzlooOmB231qMM85d2/fV6ChevvXvQP8Hkue1poOFtnEtpyxVLW1zAo6/1Xx1COxFvrc2d7UL/lmHInNlxuacJXwu0fjpXfz/YqYzBIBzD6WUfTIF9GRHpOn/Hz7saL8xz+W//FRAUid1OksQaQx4CMs8LOddcQhULW4ucetDf96JcR3g0gfRK4PC7E/r7Z6xNrXd2UIeorGj5Ef7b1pJAYB6Y5anaHqZ9J6nKEBvB4DnNLIVWSgARns/8wR2SiRS7MNACwTyrGvt9ts8p12PKFdlqYTopNHR1Vf7XjfhQlVsAJdNiKdYmYVoKlaRv85IfVunYzO0IKXsyl7JCUjCpoG20f0a04COwfneQAGGwd5oa+T8yO5hzuyDb/XcxxmK01EpqOyuxINew=='
), 'iv': json.dumps('r7BXXKkLb8qrSNn05n0qiA=='), 'token': json.dumps('7376b0ce15ca4502dd626cf16852c8f6')}

session = requests.Session()
session.headers = header

responses = session.post(url = url2, data=data2)
responses.encoding = 'utf-8'
print(responses.text)