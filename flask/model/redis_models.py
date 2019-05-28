import redis
import hmac



class Redis_db():
    '''系统用到的redis操作'''
    def __init__(self, using_mothod):
        db_list = {'token': 0, 'formId': 1, 'pushMsg_status': 2}
        self.__db = db_list.get(using_mothod, None)
        self.r, self.pipeline = self.choose_db(self.__db)
        self.__usingmothod = using_mothod

    def choose_db(self ,db):
        if db != None and isinstance(db, int):
            r = redis.Redis(
                host="127.0.0.1",
                port=6379,
                password="123456qw@", db=db,
                decode_responses=True)
            pipeline = r.pipeline()
            return (r, pipeline)
        else:
            raise Exception('db choosing Error!')

    def set_formId(self, openid, formId, overtime=518400):
        '''存放formId 默认六天过期'''
        if self.__db == 1:
            self.pipeline.set(openid, formId)
            self.pipeline.expire(openid, overtime)
            response = self.pipeline.execute()
            if response:
                return True
            else:
                return False
        else:
            raise Exception('db choosed Error!')
    def get_formId(self, openid):
        '''获取用户存放的formId 进行消息发送'''
        if self.__db == 1:
            formId = self.r.get(openid)
            self.r.delete(openid)
            # 同时删除
            return formId
        else:
            raise Exception('db choosed Error!')

    def set_pushMsg_status(self, item_id, openid, overtime=86400):
        '''记录今天 已经推送提醒用户参与活动'''
        if self.__db == 2:
            key = hmac.new(item_id, openid, digestmod='MD5').hexdigest()
            self.pipeline.set(key, 1)
            self.pipeline.expire(key, overtime)
            response = self.pipeline.execute()
            if response:
                return True
            else:
                return False
        else:
            raise Exception('db choosed Error!')

    def check_pushMsg_status(self, item_id, openid):
        '''检查是否已经推送提醒'''
        if self.__db == 2:
            key = hmac.new(item_id, openid, digestmod='MD5').hexdigest()
            status = self.r.get(key)
            if status:
                return True
            else:
                return False
        else:
            raise Exception('db choosed Error!')


# token_pipeline = r_token.pipeline()
# pipeline.hmset(self.pswd, key_dict)
# pipeline.expire(self.pswd, overtime)
# response = pipeline.execute()
