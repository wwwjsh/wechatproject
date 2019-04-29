from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
'''通过这个测试可以看出python从数据库取出time类型的数据会自动转换为python的datetime类型'''
app = Flask(__name__)
# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/test?charset=utf8"
#设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 创建数据库的操作对象
db = SQLAlchemy(app)

class Time(db.Model):
    __tablename__ = 'time'
    id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.TIMESTAMP, nullable=False)

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    times = Time.query.filter(id!=1).all()
    times2 = db.session.query(Time).filter(id!=1).all()
    print(type(times)) #datetime对象类型
    adict = {'start_time': times}
    print(times2[0].start_time)
    # print(json.dumps(adict)) 报错字典中有一个为datetime类型

