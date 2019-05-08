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
    import cv2
    from werkzeug.utils import secure_filename
    import json

    path = os.path.dirname(__file__)
    # with open(path+'/sql.txt','rb') as f:
    url  = 'https://yun.hookeii.cn/launchActivity/uploadimg'
        # print(f.read())
    files = { 'file' : (open(path+'/2.png','rb'))}
    # with open(path+'/3.png','rb') as f:
    #     print(f.read())
    data = {'formData': json.dumps({'token': '4cd19fc12727e2af8729ff7c936a02e9', 'wd':'s4ovi'})}
    url2 = 'https://yun.hookeii.cn//items'
    code = '033bgKhW0a98I22rJehW0GMKhW0bgKhd'
    data = {
        'appid': 'wx64118b44bbd3bfa3',
        'secret': '284ae53ebc924e862f12fb1e71d9a941',
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.get(url='https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code',params=data)
    print(response.text)
    # basepath = os.path.dirname(__file__)  # 当前文件所在路径
    # upload_path = basepath + 'static/images'+secure_filename('1.png')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    # print(upload_path)
    #
    # img = cv2.imread('2.png')
    # cv2.imwrite('5.jpg', img)
