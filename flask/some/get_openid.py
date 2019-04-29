import requests

def get_user_info(js_code):
    req_params = {
        "appid": 'app_id', # 小程序ID
        "secret": 'secret', # 小程序 secret
        "js_code": js_code,
        "grant_type": 'authorization_code'
    }
    req_resuLt = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code', params=req_params, timeout=3, verify=False)
    #把返回的json数据转化成dict
    return req_resuLt.json()
if __name__ == '__main__':
    import os
    import requests
    import json

    path = os.path.dirname(__file__)
    # with open(path+'/sql.txt','rb') as f:
    url  = 'http://127.0.0.1:5000/launchActivity/uploadimg'
        # print(f.read())
    files = { 'file' : (open(path+'/3.png','rb'))}
    with open(path+'/3.png','rb') as f:
        print(f.read())
    data = {'formData': json.dumps({'token': '8e4e17a9dfe24bca4314a0b09ba1af8d', 'wd':'s4ovi'})}
    response = requests.post(url=url, data=data, files = files)
    print(response.text)