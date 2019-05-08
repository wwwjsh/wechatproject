import os
import requests

url = 'https://yun.hookeii.cn/launchActivity/uploadimg'

path = os.path.dirname(__file__) #获取该执行文件的路径
files = {'file': (open(path + '/2.png', 'rb'))}
data = {'参数': '数值'}
params = {'参数': '数值'}
response = requests.post(url=url, data=data, files=files) #发post请求上传文件
response2 = requests.get(url=url, params=params)
# response.encoding('utf-8')
print(response.text) # 打印文格式的返回信息 乱码就该utf-8编码
print(response2.text)