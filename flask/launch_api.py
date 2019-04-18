from flask import Blueprint, abort, json, request
from ord_models import *
import random
import datetime
'''from flask import Blueprint,render_template
#创建蓝图
logins = Blueprint('login',__name__)

@logins.route('/login')
def login(): 
    return render_template('login.html')'''
launch = Blueprint('launch', __name__)
def generate_random_str(randomlength=5):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'abcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

#发起活动链接到数据库
@launch.route('/launchActivity',methods=['POST'])
def lau_item():
    #json.loads(request.values.get("txt3"))
    #items表添加元素
    lau_usId = str(json.loads(request.values.get("lau_usId")))
    item_name = str(json.loads(request.values.get("item_name"))) #
    pass_id = generate_random_str(5)
    item_type = str(json.loads(request.values.get("item_type")))
    contacts = str(json.loads(request.values.get("contacts")))
    start_time = str(json.loads(request.values.get("start_time")))
    end_time = str(json.loads(request.values.get("end_time")))
    item_address = str(json.loads(request.values.get("item_address")))
    text_info = str(json.loads(request.values.get("text_info")))
    ord_objects = json.loads(request.values.get("ord_objects"))
    newItem = Item(lau_usId = lau_usId, item_name = item_name, pass_id = pass_id, item_type = item_type, contacts = contacts, \
                   start_time = start_time, end_time = end_time, item_address = item_address, text_info = text_info)
    db.session.add(newItem)
    db.session.commit()
    objlist = []
    # print([start_time,end_time])
    for object in ord_objects:
        #遍历所有预定对象，例如五张桌子，遍历每张桌子
        time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        while time < end:
            #切割小时间段
            newObj = OrdObject(itemId = newItem.item_id, obj_num = object["obj_num"], obj_name = object["obj_name"],\
                               minOrd_time = object["minOrd_time"], startOrd_time = str(time), ordable_sum = object["ordable_sum"], residue = object["ordable_sum"])
            objlist.append(newObj)
            time = time + datetime.timedelta(minutes=object["minOrd_time"])
        #ord_objects: [{obj_num: int(3), obj_name: varchar(15), minOrd_time: time, ordable_sum: int(3)}]}
    db.session.add_all(objlist)
    db.session.commit()
    return "OK"
