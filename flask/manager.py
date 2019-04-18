from flask import Flask
#导入蓝图对象
from launch_api import launch

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
#注册蓝图，第一个参数logins是蓝图对象，url_prefix参数默认值是根路由，如果指定，会在蓝图注册的路由url中添加前缀。
app.register_blueprint(launch,url_prefix='')

if __name__ == '__main__':
    app.run(debug=True)