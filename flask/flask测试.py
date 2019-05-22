'''单元测试文件'''

import unittest
from manager import *
from flask import json
import os
import requests

tojs = json.dumps


class home_test(unittest.TestCase):
    '''测试主页用例'''

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_homepage(self):
        """测试主页的返回
        info = {'data': items_todict,"errNum": 0, "errMsg": "success"}"""
        response = app.test_client().post('/items', json={'code': '233333'})
        # json_data = response.data
        json_dict = response.get_json()
        print('首页api')
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')
        self.assertEqual(type(json_dict), dict, '数据类型错误')


def newuser():
    response = app.test_client().post('/newuser', json={'code': '233333'})
    json_data = response.data
    json_dict = json.loads(json_data)
    token = json_dict['User_token']
    print('新用户登录,老用户更新token api')
    print(json_dict['User_token'])
    return token


class Login_test(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.token = newuser()

    # def test_newuser(self):
    #     '''测试新用户注册和老用户获取token的接口'''
    #
    #     data = result.newuser()
    #     self.assertIn("errNum", data, '数据错误缺少参数errNum')
    #     self.assertEqual(data['errNum'], 0, '状态码错误')
    #     self.assertIn('User_token', data, '微信服务器错误')

    def test_update_address(self):
        '''测试用户更新地址'''
        self.assertEqual(len(self.token), 32, 'token获取错误')
        print(type(self.token))
        response = app.test_client().post(
            '/user/update',
            json={
                'token': self.token,
                'address': "广tm",
                'phone': ''})
        json_data = response.get_json()
        json_dict = response.get_json()
        print('用户更新地址信息 api')

        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误, 用户不存在')

    def test_update_phone(self):
        '''测试用户更新电话号码'''
        response = app.test_client().post(
            '/user/update',
            json={
                'token': self.token,
                'address': "",
                'phone': '88888'})
        json_data = response.data
        json_dict = json.loads(json_data)
        print('用户更新电话信息 api')
        print(type(json_dict))
        print({'gg': json_dict})
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误, 用户不存在')

    def test_update_phoneandadress(self):
        '''测试用户更新电话号码和地址'''

        response = app.test_client().post(
            '/user/update',
            json={
                'token': self.token,
                'address': '变成上海',
                'phone': '12222'})
        json_dict = response.get_json()
        print('用户同时更新两个信息 api')
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')

    def test_updateuserinfo(self):
        '''修改用户的头像和昵称，获取私密信息'''
        response = app.test_client().post(
            '/userinfo',
            json={
                'token': self.token,
                'encryptedData': 'CiyLU1Aw2KjvrjMdj8YKliAjtP4gsMZMQmRzooG2xrDcvSnxIMXFufNstNGTyaGS9uT5geRa0W4oTOb1WT7fJlAC+oNPdbB+3hVbJSRgv+4lGOETKUQz6OYStslQ142dNCuabNPGBzlooOmB231qMM85d2/fV6ChevvXvQP8Hkue1poOFtnEtpyxVLW1zAo6/1Xx1COxFvrc2d7UL/lmHInNlxuacJXwu0fjpXfz/YqYzBIBzD6WUfTIF9GRHpOn/Hz7saL8xz+W//FRAUid1OksQaQx4CMs8LOddcQhULW4ucetDf96JcR3g0gfRK4PC7E/r7Z6xNrXd2UIeorGj5Ef7b1pJAYB6Y5anaHqZ9J6nKEBvB4DnNLIVWSgARns/8wR2SiRS7MNACwTyrGvt9ts8p12PKFdlqYTopNHR1Vf7XjfhQlVsAJdNiKdYmYVoKlaRv85IfVunYzO0IKXsyl7JCUjCpoG20f0a04COwfneQAGGwd5oa+T8yO5hzuyDb/XcxxmK01EpqOyuxINew==',
                'iv': 'r7BXXKkLb8qrSNn05n0qiA=='})
        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')


class launch_test(unittest.TestCase):
    '''测试用户发起活动是否能行'''

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.token = newuser()

    def test_launchactivaty(self):
        '''测试用户发起一个项目'''
        data = {"item_name": '中心湖公园玩耍', "item_type": '1',  # 1排队类型
                "contacts": 'qq:11111555', "timetable": [{'start_date': '2012-05-08', 'end_date': '2012-05-10', 'start_time': '14:00', 'end_time': '16:00'}],
                "address": "中心湖公园",
                "text_info": '大家记得来啊！', "objs":
                # [号码，预定对象的名称，最小预定时间，单位最小预定时间可预订的数量}
                [{'obj_num': 0, 'obj_name': '三号场', 'minOrd_time': 60, 'ordable_sum': 30},
                 {'obj_num': 1, 'obj_name': '四号场', 'minOrd_time': 60, 'ordable_sum': 30}]}
        response = app.test_client().post('/launchActivity',
                                          json={'token': self.token,
                                                'data': data})
        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')
    # def test_uploadimg(self):
    #     '''测试用户上传文件'''
    #     url = 'http://127.0.0.1:5000/launchActivity/uploadimg'
    #     path = os.path.dirname(__file__)
    #     with open(path + '/2.png', 'rb') as f:
    #         temp = f
    #     try:
    #         files = {'file': temp}
    #         r = requests.post(url, files=files)
    #     except:
    #         print(0)


class join_test(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.token = newuser()

    def test_join_info(self):
        '''测试是否能获取指定项目的预定信息 '''
        response = app.test_client().get(
            '/joinInfo?wd=gy56k', data={'wd': 'gy56k'})
        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')

    def test_joinitem1(self):
        '''测试预定可预定对象，情况： 都有剩余位置 '''
        response = app.test_client().post(
            '/joinAcitvity',
            json={
                'token': self.token,
                'objId': [
                    84,
                    85]})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')

    def test_joinitem2(self):
        '''测试预定可预定对象，情况： 都没有剩余位置 '''
        response = app.test_client().post(
            '/joinAcitvity',
            json={
                'token': self.token,
                'objId': [
                    105,
                    106]})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], -1, '状态码错误')
        self.assertEqual(
            json_dict["errMsg"],
            'ObjresidueError.',
            '有对象被成功预定了 错误的情况被通过')

    def test_joinitem3(self):
        '''测试预定可预定对象，情况： 其中一个没有剩余位置 '''
        response = app.test_client().post(
            '/joinAcitvity',
            json={
                'token': self.token,
                'objId': [
                    104,
                    103]})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], -1, '状态码错误')
        self.assertEqual(
            json_dict["errMsg"],
            'ObjresidueError.',
            '有对象被成功预定了 错误的情况被通过')


class test_iteminfo(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.token = newuser()

    def test_mylauchitem(self):
        '''测试用户获取自己发起的项目的信息列表 成功情况'''
        response = app.test_client().post(
            '/iteminfo/Mylaunch', json={'token': self.token})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')
    # def test_mylauchitem2(self):
    #     '''测试用户获取自己发起的项目的信息列表 错误情况'''
    #     response = app.test_client().post('/iteminfo/Mylaunch', json={'token': self.token})
    #
    #     json_dict = response.get_json()
    #     print(json_dict)
    #     self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
    #     self.assertEqual(json_dict['errNum'], -1, '状态码错误')

    def test_mylauchitemdetail(self):
        '''测试获取自己的项目详情信息'''
        response = app.test_client().post(
            '/iteminfo/Mylaunch/detail',
            json={
                'token': self.token,
                'wd': 'gba21'})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')

    def test_mylauchitemdetail2(self):
        '''测试获取自己的项目详情信息 情况错误的wd'''
        response = app.test_client().post(
            '/iteminfo/Mylaunch/detail',
            json={
                'token': self.token,
                'wd': 'gba421'})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], -1, '状态码错误')

    def test_myjoineditem(self):
        '''测试获取自己的加入项目'''
        response = app.test_client().post(
            '/iteminfo/Myjoined', json={'token': self.token})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')

    # def test_myjoineditem2(self):
    #     '''测试获取自己的加入项目 情况2 没有加入的项目'''
    #     response = app.test_client().post('/iteminfo/Myjoined', json={'token': self.token})
    #
    #     json_dict = response.get_json()
    #     print(json_dict)
    #     self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
    #     self.assertEqual(json_dict['errNum'], 0, '状态码错误')
    def test_myjoineditemdetali(self):
        '''测试获取自己的加入项目 '''
        response = app.test_client().post(
            '/iteminfo/Myjoined/detail',
            json={
                'token': self.token,
                'wd': 'pysnr'})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], 0, '状态码错误')

    def test_myjoineditemdetali2(self):
        '''测试获取自己的加入项目 情况 不是自己加入的项目 错误的项目号'''
        response = app.test_client().post(
            '/iteminfo/Myjoined/detail',
            json={
                'token': self.token,
                'wd': 'gba421'})

        json_dict = response.get_json()
        print(json_dict)
        self.assertIn("errNum", json_dict, '数据错误缺少参数errNum')
        self.assertEqual(json_dict['errNum'], -1, '状态码错误')
        self.assertEqual(json_dict['errMsg'], 'itemError.', '返回的不是项目错误')


if __name__ == '__main__':
    unittest.main()
    # uite = unittest.TestSuite()
    # suite.addTest(login_Test.parametrize(TestOne, param=42))
    # suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=13))
    # unittest.TextTestRunner(verbosity=2).run(suite)
