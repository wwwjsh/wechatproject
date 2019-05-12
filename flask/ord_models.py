'''数据orm对象生成和操作'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
'''数据库模型文件'''
app = Flask(__name__)
# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/ord?charset=utf8"
#设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 创建数据库的操作对象
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True)
    nickname = db.Column(db.String(30))
    avatarurl = db.Column(db.String(200))
    openid = db.Column(db.CHAR(128), nullable=False, unique=True, index=True)
    unionid = db.Column(db.CHAR(128))
    address = db.Column(db.String(60))
    phone = db.Column(db.CHAR(11))


class Item(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.INTEGER, primary_key=True)
    item_name = db.Column(db.String(20), nullable=False)
    pass_id = db.Column(db.CHAR(5), nullable=False, unique=True)
    lau_usId = db.Column(db.ForeignKey('users.openid'),  nullable=False, index=True)
    item_type = db.Column(db.Enum('1', '2'), nullable=False)
    contacts = db.Column(db.String(20), nullable=False)
    contacter = db.Column(db.String(20))
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    item_address = db.Column(db.String(60))
    text_info = db.Column(db.String(150))
    img_info = db.Column(db.String(100))
    page_show = db.Column(db.INTEGER, server_default=db.text("'1'"))
    logic_del = db.Column(db.INTEGER, server_default=db.text("'1'"))
    lau_time = db.Column(db.TIMESTAMP, server_default=db.text("CURRENT_TIMESTAMP"))

    user = db.relationship('User')
'''字段 ：item_id item_name pass_id lau_usId item_type contacts start_time end_time item_address text_info img_info page_show'''

class OrdObject(db.Model):
    __tablename__ = 'ord_objects'

    obj_id = db.Column(db.INTEGER, primary_key=True)
    itemId = db.Column(db.ForeignKey('items.item_id'),  nullable=False, index=True)
    obj_num = db.Column(db.INTEGER, nullable=False)
    obj_name = db.Column(db.String(15))
    minOrd_time = db.Column(db.INTEGER, nullable=False)
    startOrd_time = db.Column(db.DateTime, nullable=False)
    ordable_sum = db.Column(db.INTEGER, nullable=False)
    residue = db.Column(db.INTEGER, nullable=False)
    logic_del = db.Column(db.INTEGER, server_default=db.text("'1'"))

    item = db.relationship('Item')
'''字段：obj_id itemId obj_num obj_name minOrd_time startOrd_time ordable_sum residue'''

class Order(db.Model):
    __tablename__ = 'orders'

    ord_num = db.Column(db.INTEGER, primary_key=True)
    ord_itemId = db.Column(db.ForeignKey('items.item_id'),  nullable=False)
    ord_usId = db.Column(db.ForeignKey('users.openid'), nullable=False, index=True)
    ord_price = db.Column(db.INTEGER, server_default=db.text("'0'"))
    pay_status = db.Column(db.Enum('0', '1'), server_default=db.text("'0'"))
    place_time = db.Column(db.TIMESTAMP, server_default=db.text("CURRENT_TIMESTAMP"))
    cancel_del = db.Column(db.INTEGER, server_default=db.text("'1'"))

    item = db.relationship('Item') # 用户取消加入活动 需要添加一个外键 通过连接修改该字段 查询信息自己加入的时候 使用两个子链接 再进行内连接
    user = db.relationship('User')

class Orderinfo(db.Model):
    __tablename__ = 'orderinfo'

    ord_id = db.Column(db.INTEGER, primary_key=True)
    ordNum = db.Column(db.ForeignKey('orders.ord_num'), nullable=False)
    objId = db.Column(db.ForeignKey('ord_objects.obj_id'),  nullable=False, index=True)
    queue_num = db.Column(db.INTEGER, server_default=db.text("'-1'"))
    ord_object = db.relationship('OrdObject')

    order = db.relationship('Order')

    db.create_all()
if __name__ == '__main__':
    #db.drop_all()
    db.create_all()
    # user = db.session.query(User).filter(User.id==1).first()
    # user.nickname = '改一下1'
    # db.session.commit()
    # user.address = '再改1'
    # db.session.commit()
    # db.session.rollback()
    # times2 = db.session.query(Time).filter(id != 1).all()

    '''s = db.session.query(OrdObject,Item).\
        filter(Order.ord_usId=='123456').\
        all()
    print(dir(s[0]))
    print(len(s)) #从多表中查询
    print(dir(s[0].OrdObject))
    print(s[0].OrdObject.obj_id)'''
    '''item =db.session.query(Item).filter(Item.item_id.in_(db.session.query(OrdObject.itemId).filter(OrdObject.obj_id.in_
                                                                                             (db.session.query(
                                                                                                 Orderinfo.objId).filter(
                                                                                                 Orderinfo.ordNum.in_
                                                                                                 (db.session.query(
                                                                                                     Order.ord_num).filter(
                                                                                                     Order.ord_usId == '123456')
                                                                                                  )))))).all()
    print(item[0].item_id) # 查询用户加入的项目'''
    #db.session.query(Orderinfo).filter(Orderinfo.ordNum.in_(db.session.query(Order.ord_num).filter(Order.ord_usId == '123456'))).all()
        # filter(Order.ord_usId != 1, Order).\


    # db.session.query(Item).outjoin(O)
    # cursor = db.session.execute('insert into users (nickname,openid,unionid,session_key, address, phone)values("Jhon","123456","1234567","er4t5s","广州", "1552119220");')
    # cursor = db.session.execute(
    #     'insert into users (nickname,openid,unionid,session_key, address, phone)values("shala","456123","1234567","er4t5s","柳州", "15521192220");')
    # # result = cursor.fetchall()
    # cursor.close()
    #item = Item.query.filter_by(pass_id = "hg7v0").first()

    #obj_timelist = [str(i)for i in OrdObject.query.filter_by(itemId= item.item_id).with_entities(OrdObject.startOrd_time).distinct().all()]
    #print(obj_timelist)
    # def test():
    # cur = db.session.execute("select * from users")
    # result = cur.fetchall()
    # print(type(result))
    # cur.close()
    # test()
        # us1 = User(nickname = "John", openid = "agwre123",session_key = "e54t24",address = "广州市", phone = "15521192220")
    # db.session.add(us1)
    # db.session.commit()
    # app.run(debug=True)