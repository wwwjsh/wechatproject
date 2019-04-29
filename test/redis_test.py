import redis

#连接redis数据库，host port password 字符/字节存入 选择字符存入操作
r = redis.Redis(host="127.0.0.1", port=6379, password="123456qw@", decode_responses=True)

#设置管道
pipeline = r.pipeline()

#发送到redis服务器函数
def token_sendtoredis(token, session_key, openid,overtime):
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

if __name__ == '__main__':
    #
    # #保存数据
    session_key = 'tiihtNczf5v6AKRyjwEUhQ=='
    openid = 'oGZUI0egBJY1zhBYw2KhdUfwVJJE'
    # #token的时效
    overtime = 600
    key_dict = {'session_key': session_key, 'openid': openid}
    #
    # #放入管道 哈希类型
    pipeline.hmset('7376b0ce15ca4502dd626cf16852c8f6', key_dict)
    # pipeline.expire('7376b0ce15ca4502dd626cf16852c8f6', overtime)
    respone = pipeline.execute()
    # rs = r.hget("7376b0ce15ca4502dd626cf16852c8f6", 'openid')
    e = r.exists("123") # 返回0或者1
    # #返回是否成功，是一个列表
    print(respone)
    # print(type(e))


