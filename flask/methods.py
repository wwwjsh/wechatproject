'''在项目中使用的方法 类 装饰器'''

import json
from datetime import datetime, date
import random
import requests
import base64
from Crypto.Cipher import AES
import redis
import hmac
import secrets
from flask import jsonify
from functools import wraps
from ord_models import db

# 配置小程序appid和secret
appid = 'wx64118b44bbd3bfa3'
secret = '9ca7dc56b74663931643555302ef90e5'

#连接redis数据库，host port password 字符/字节存入 选择字符存入操作
r = redis.Redis(host="127.0.0.1", port=6379, password="123456qw@", decode_responses=True)
pipeline = r.pipeline()

#encryptedDatay用户私密数据的解密器
class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
# 日期这转化成列表
def datetime_to_list(datetime):
    return [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute]

#日期类型转换成json数据
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def try_db_commit(ins):
        try:
            db.session.add(ins)
            db.session.commit()
            info = {"errNum": 0, "errMsg": "success"}
            return jsonify(info)
        except:
            info = {"errNum": -1, "errMsg": "dbError"}
            return jsonify(info)

# 获取用户的opendid和session_key，openid
def get_user(js_code, app_id=appid, secret=secret):
    # 执行测试 所用的数据
    # return {'openid': 'bbbUI0egBJY1zhBYw2KhdUfwVJJE', 'session_key': 'tiihtNczf5v6AKRyjwEUhQ==', 'errcode': 0}
    url = ' https://api.weixin.qq.com/sns/jscode2session'
    req_params = {
        "appid": app_id, # 小程序ID
        "secret": secret, # 小程序 secret
        "js_code": js_code,
        "grant_type": 'authorization_code'
    }

    req_resuLt = requests.get(url=url, params=req_params, timeout=3, verify=False)

    # 把返回的json数据转化成dict,返回字典类型
    return req_resuLt.json()


#生成指定长随机串
def generate_random_str(randomlength=5):
    random_str = ''
    base_str = 'abcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str



#token处理对象类
class Token():
    '''包括验证token密钥，生成token的密钥，根据token密钥查找opendid,session_key的方法'''
    def __init__(self, openid=None, session_key=None, token=None):
        self.openid = openid
        self.session_key = session_key
        self.pswd = token
        self.checked = False #0未通过验证 1通过验证 flask 未验证

    def checkbytoken(self,func): #通过路由请求，验证登录状态
        @wraps(func)
        def decorated(data):
            data = data if type(data)==dict else data.get_json()
            print(data)

            if data and data.get('token', 0):
                self.pswd = data['token']
                if self.check():
                    data['token'] = self
                    return func(data)
                else:
                    return jsonify({"errNum": -1, 'errMsg': "tokenError"})

            else:
                return jsonify({"errNum": -1, 'errMsg': "token inexistence form Error"})
        return decorated

    # def filesrequests_checktoken(self, func):
    #     # print(type(json.loads(request.values.get('formData'))))
    #     @wraps(func)
    #     def decorated(data):
    #         data = data.get('token')
    #         if data:
    #             if self.check():
    #                 data['token'] = self
    #                 return func(data)
    #             else:
    #                 return jsonify({"errNum": -1, 'errMsg': "tokenError"})

    def check(self):
        self.checked = r.exists(self.pswd)
        return self.checked

    def token_sendtoredis(self, overtime=6000): # 发送到数据库
        # arg all str
        key_dict = {'session_key': self.session_key, 'openid': self.openid}
        pipeline.hmset(self.pswd, key_dict)
        pipeline.expire(self.pswd, overtime)
        try:
            response = pipeline.execute()
            # response = [True, True]
            result = [i for i in response if i is not True]
            #存入成功
            if not result:
                return self.pswd
            else:
                return ({"errNum": -1, 'errMsg': "redis error"})
        except:
            raise Exception('Invalid Buffer')

    def set_pawd(self, sendto_redis=True, overtime=6000): #生成token令牌并且存入数据库
        openid = bytes(self.openid, encoding='utf-8')
        key = secrets.token_bytes(16)
        self.pswd = hmac.new(key, openid, digestmod='MD5').hexdigest()
        if sendto_redis: #成功 返回pswd
            result = self.token_sendtoredis(overtime)
            return result
        return False #失败返回Flase

    def get_openid(self, auto_check=True): #凭令牌获取用户的openID
        if auto_check:
            self.check()
        if self.checked:
            self.openid = r.hget(self.pswd, 'openid')
            return self.openid
        else:
            print("please checked!")
            return None

    def get_session_key(self, auto_check=True): #凭令牌获取用户的session_key
        if auto_check:
            self.check()
        if self.checked:
            self.session_key = r.hget(self.pswd, 'session_key')
            return self.session_key
        else:
            print("please checked!")
            return None
