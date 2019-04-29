'''对哈希生成令牌'''
import redis
import hmac
import secrets
from methods import generate_random_str
openid = bytes("",encoding='utf-8')
key = secrets.token_bytes(5)
h = hmac.new(key, openid, digestmod='MD5')
print(len(h.hexdigest()))#32位字符串类型

openid = 'oGZUI0egBJY1zhBYw2KhdUfwVJJE'

#对获取token方法
def get_token(openid):
    openid = bytes(openid, encoding='utf-8')
    key = secrets.token_bytes(16)
    h = hmac.new(key, openid, digestmod='MD5')
    return h

#连接redis数据库，host port password 字符/字节存入 选择字符存入操作
r = redis.Redis(host="127.0.0.1", port=6379, password="123456qw@", decode_responses=True)

#设置管道
pipeline = r.pipeline()

#发送到redis服务器函数
def token_sendtoredis(token, session_key, openid, overtime = 600):
    #arg all str
    key_dict = {'session_key': session_key, 'openid': openid}
    pipeline.hmset(token, key_dict)
    pipeline.expire(token, overtime)
    respone = pipeline.execute()
    return respone

#从redis中通过token 返回用户openID
def token_getopid(token):
    openid = r.hget(token, 'openid')
    return openid

class Token():
    '''包括验证token密钥，生成token的密钥，根据token密钥查找opendid,session_key的方法'''
    def __init__(self, openid=None, session_key=None, token=None):
        self.openid = openid
        self.session_key = session_key
        self.pswd = token
        self.checked = False #0未通过验证 1通过验证 flask 未验证

    def check(self): #被验证的状态
        self.checked = r.exists(self.pswd)
        return self.checked

    def token_sendtoredis(self, overtime=600): # 发送到数据库
        # arg all str
        key_dict = {'session_key': self.session_key, 'openid': self.openid}
        pipeline.hmset(self.pswd, key_dict)
        pipeline.expire(self.pswd, overtime)
        try:
            respone = pipeline.execute()
            # response = [True, True]
            result = [i for i in respone if i is not True]
            #存入成功
            if not result:
                return self.pswd
            else:
                return "redis error"
        except:
            raise Exception('Invalid Buffer')

    def set_pawd(self, sendto_redis=True, overtime=600): #生成token令牌并且存入数据库
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


token = Token(openid='oGZUI0egBJY1zhBYw2KhdUfwVJJE', session_key='tiihtNczf5v6AKRyjwEUhQ==')
print(type(get_token('oGZUI0egBJY1zhBYw2KhdUfwVJJE')))
print(token.set_pawd().openid)