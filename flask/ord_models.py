# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
'''数据库模型文件'''
app = Flask(__name__)
# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/ord?charset=utf8"
#设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 创建数据库的操作对象
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True)
    nickname = db.Column(db.String(30))
    openid = db.Column(db.CHAR(128), nullable=False, unique=True)
    unionid = db.Column(db.CHAR(128))
    session_key = db.Column(db.CHAR(128))
    address = db.Column(db.String(60))
    phone = db.Column(db.CHAR(11))


class Item(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.INTEGER, primary_key=True)
    item_name = db.Column(db.String(20), nullable=False)
    pass_id = db.Column(db.CHAR(5), nullable=False, unique=True)
    lau_usId = db.Column(db.ForeignKey('users.openid'), index=True)
    item_type = db.Column(db.Enum('1', '2'), nullable=False)
    contacts = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    item_address = db.Column(db.String(60))
    text_info = db.Column(db.String(150))
    img_info = db.Column(db.String(100))
    lau_time = db.Column(db.TIMESTAMP, server_default=db.text("CURRENT_TIMESTAMP"))

    user = db.relationship('User')


class OrdObject(db.Model):
    __tablename__ = 'ord_objects'

    obj_id = db.Column(db.INTEGER, primary_key=True)
    itemId = db.Column(db.ForeignKey('items.item_id'), index=True)
    obj_num = db.Column(db.INTEGER, nullable=False)
    obj_name = db.Column(db.String(15))
    minOrd_time = db.Column(db.INTEGER, nullable=False)
    startOrd_time = db.Column(db.DateTime, nullable=False)
    ordable_sum = db.Column(db.INTEGER, nullable=False)
    residue = db.Column(db.INTEGER, nullable=False)
    logic_del = db.Column(db.INTEGER, server_default=db.text("'1'"))

    item = db.relationship('Item')


class Order(db.Model):
    __tablename__ = 'orders'

    ord_id = db.Column(db.INTEGER, primary_key=True)
    ord_num = db.Column(db.INTEGER, nullable=False)
    objId = db.Column(db.ForeignKey('ord_objects.obj_id'), index=True)
    ord_usId = db.Column(db.ForeignKey('users.openid'), index=True)
    queue_num = db.Column(db.INTEGER, server_default=db.text("'-1'"))
    place_time = db.Column(db.TIMESTAMP, server_default=db.text("CURRENT_TIMESTAMP"))

    ord_object = db.relationship('OrdObject')
    user = db.relationship('User')

    db.create_all()
if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    # cursor = db.session.execute("select * from users")
    # result = cursor.fetchall()
    # print(result)
    # def test():
    #     cur = db.session.execute("select * from users")
    #     result = cur.fetchall()
    #     print(result)
    #     cur.close()
    # test()
        # us1 = User(nickname = "John", openid = "agwre123",session_key = "e54t24",address = "广州市", phone = "15521192220")
    # db.session.add(us1)
    # db.session.commit()
    # app.run(debug=True)