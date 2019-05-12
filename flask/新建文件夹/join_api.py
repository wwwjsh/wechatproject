'''用户执行加入操作时调用的api'''

from flask import Blueprint, json, request, jsonify
from ord_models import *
from methods import DateEncoder, Token, try_db_commit
import datetime
#创建蓝图
join = Blueprint('join', __name__)
token = Token()

@join.route('/joinInfo', methods=['POST'])
def join_info():
    pass_id = request.get_json().get("wd", 0)
    #查找对应的项目
    if pass_id:
        #User.query.filter(User.name!='wang').all()
        item = Item.query.filter_by(pass_id=pass_id).first()
        if item:
            lau_user = User.query.filter_by(openid=item.lau_usId).first()
            if lau_user:
                obj_time_distin = db.session.query(OrdObject.startOrd_time).filter(OrdObject.itemId == item.item_id).distinct().order_by(OrdObject.startOrd_time).all()
                # print(obj_time_distin)
                # print(obj_time_distin.all()[0].startOrd_time)
                # obj_timelist = OrdObject.query.filter_by(itemId= item.item_id).with_entities(OrdObject.startOrd_time).distinct().order_by(OrdObject.startOrd_time)
                obj_data = [{"start_time": obj_time[0],
                             "obj": [{"obj_id": i.obj_id,"obj_name": i.obj_name,
                                      "minOrd_time": i.minOrd_time,"residue": i.residue}
                                     for i in db.session.query(OrdObject).filter(OrdObject.startOrd_time == obj_time,
                                                                                 OrdObject.itemId == item.item_id).all()]}
                            for obj_time in obj_time_distin]

                date_list = []
                dealed_data = []
                for data in obj_data:
                    date = [data['start_time'].year, data['start_time'].month, data['start_time'].day]
                    data['start_time'] = [ data['start_time'].hour, data['start_time'].minute]  # 修改开始时间格式
                    # print(date) # 返回日期列表
                    if date not in date_list:
                        date_list.append(date)
                        dealed_data.append({'date': date, 'objs': [data]})
                    else:
                        for i in range(len(dealed_data)):
                            if dealed_data[i].get('date', 0) == date:
                                dealed_data[i]['objs'].append(data)

                datadict = {"item_name": item.item_name, "item_type": item.item_type, "pass_id": item.pass_id, "start_time": json.dumps(item.start_time, cls=DateEncoder),
                        "end_time": json.dumps(item.end_time, cls=DateEncoder), "contacter": lau_user.nickname, "contacts": item.contacts,
                        "item_address": item.item_address, "text_info": item.text_info, "img_info": item.img_info,
                        "lau_time": json.dumps(item.lau_time, cls=DateEncoder), "obj_data": dealed_data}
                # print(obj_data[0]['start_time'][0].year) # 时间对象返回年
                print(dealed_data)
                info = {'data': datadict, "errNum": 0, "errMsg": "success"}
                db.session.close()
                return jsonify(info)
            else:
                db.session.close()
                info = {"errNum": -1, "errMsg": "lau_userError"}
                return jsonify(info)
    else:
        db.session.close()
        info = {"errNum": -1, "errMsg": "pass_idError"}
        return jsonify(info)


@join.route('/joinAcitvity',methods=['POST'])
def join_item():
    '''openid = 123456
ord_price = 0
objId = [2,5]
data = {
"ord_usId" : json.dumps(openid),
"ord_price" : json.dumps(ord_price),
"objId" :  json.dumps(objId),
}'''
    @token.checkbytoken
    def decorated(data):
        #解析json数据
        ord_usId = data['token'].get_openid()
        objIds = data.get("objId",0)
        ord_price = data.get("ord_price",0)
        # 存在空表单
        if not (objIds and ord_price):
            '''还要考虑发起人和参与人是同一用户会错误'''
            #查询加入的是哪个项目 bug 判断对象不属于同一个项目下
            item = db.session.query(Item).filter(OrdObject.obj_id.in_(objIds)).filter(OrdObject.item).first()
            #创建订单
            neword = Order(ord_itemId = item.item_id ,ord_usId=ord_usId, ord_price=ord_price)
            db.session.add(neword)
            db.session.flush()
            try:
                ordinfos = []
                flag = 0 #用户预定的对象是否已经没有位置了
                for objId in objIds:
                    #该被预定的预订对象-1，计算队号
                    orded_obj = db.session.query(OrdObject).get(objId)
                    if orded_obj.residue > 0:
                        orded_obj.residue -= 1 #存在问题:多用户在高并发的情况下对同一数据进行操作可能会返回错误的队号
                        db.session.add(orded_obj)
                        queue_num = orded_obj.ordable_sum - orded_obj.residue
                        #创建被预定的订单详情
                        newordinfo = Orderinfo(ordNum=neword.ord_num, objId=objId, queue_num=queue_num)
                        ordinfos.append(newordinfo)
                    else:
                        flag = 1
                        break
                if flag == 1:
                    # 只要有一个对象不能预定 全都不预定
                    db.session.rollback()
                    db.session.close()
                    info = {"errNum": -1, "errMsg": "ObjresidueError."}
                    return jsonify(info)

                else:
                    try:
                        # 加入订单详情信息表
                        db.session.add_all(ordinfos)
                        db.session.commit()
                        info = {"errNum": 0, "errMsg": "success", "item_name": item.item_name, "address": item.item_address}
                        db.session.close()
                        return jsonify(info)
                    except:
                        db.session.close()
                        info = {"errNum": -1, "errMsg": "dbError."}
                        return jsonify(info)
            except:
                db.session.close()
                info = {"errNum": -1, "errMsg": "InvalidError."}
                #返回失败
                return jsonify(info)
        else:
            db.session.close()
            info = {"errNum": -1, "errMsg": "keyError"}
            return jsonify(info)
    return decorated(request)

