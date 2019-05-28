'''主程序执行文件
flask版本1.0.0
sqlalchemy版本2.0.0
'''

from flask import Flask
# 导入蓝图对象
from launch_api import launch
from join_api import join
from login import login
from iteminfo_api import iteminfo
from homepage_api import homepage
from collect_formId import collect_formId

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# 注册蓝图，第一个参数logins是蓝图对象，url_prefix参数默认值是根路由，如果指定，会在蓝图注册的路由url中添加前缀。
app.register_blueprint(launch, url_prefix='')
app.register_blueprint(join, url_prefix='')
app.register_blueprint(login, url_prefix='')
app.register_blueprint(homepage, url_prefix='')
app.register_blueprint(iteminfo, url_prefix='/iteminfo')
app.register_blueprint(collect_formId, url_prefix='')


if __name__ == '__main__':
    app.run(debug=False, threaded=True)
