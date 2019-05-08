'''查看项目信息要调用的api，包括用户查看我加入的项目信息和我发起的项目信息'''

from flask import Blueprint, json, request, jsonify
from ord_models import *
from methods import DateEncoder, Token, datetime_to_list
import datetime


iteminfo = Blueprint('iteminfo', __name__)
token = Token()


@iteminfo.route('/Mylaunch', methods=['POST'])
def mylaunch_itemlist():
    @token.checkbytoken
    def decorated(data):
        itemlist = db.session.query(Item).filter(Item.lau_usId == data['token'].get_openid()).all()
        if itemlist:
            '''item字段 ：item_id item_name pass_id lau_usId item_type
             contacts start_time end_time item_address text_info img_info page_show'''
            # item_todict = [{'item_name':item.item_name, 'pass_id': item.pass_id,'item_type': item.item_type,
            #                 'contacts': item.contacts, 'start_time': json.dumps(item.start_time, cls=DateEncoder),
            #                 'end_time': json.dumps(item.end_time, cls=DateEncoder), 'item_address': item.item_address,
            #                 'text_info':item.text_info, 'img_info': [], 'page_show': item.page_show}
            #                for item in itemlist]非详情页不需要这么多信息
            # 返回项目名称，项目口令 项目类型 是否过期 是否被逻辑删除（被用户取消）
            item_todict = [{'item_name':item.item_name, 'pass_id': item.pass_id,'item_type': item.item_type, 'text_info': item.text_info,
                            'overed': (item.end_time<datetime.datetime.now()), 'logic_del': item.logic_del} for item in itemlist]
            info = {'data': item_todict, "errNum": 0, "errMsg": "success"}
            print(info)
            return jsonify(info)
        else:
            info = {"errNum": -1, "errMsg": "itemNull."}
            print(info)
            return jsonify(info)
    return decorated(request)


# select * from items where items.item_id =
# (select ord_objects.itemId from ord_objects where ord_objects.obj_id =
# (select orderinfo.objId from orderinfo where orderinfo.ordNum = (
# select orders.ord_num from orders where orders.ord_usId=123456)));#多子查询嵌套得到用户加入的项目
# res=session.query(UserModel.name).filter(UserModel.id.in_(
#     session.query(UserModel.id).filter(UserModel.follow_id == UserModel.id),
# )).all()

# 查看我发起的某个项目的详情
@iteminfo.route('/Mylaunch/detail', methods=['POST'])
def mylaunch_itemdetail():
    @token.checkbytoken
    def decorated(data):
        pass_id = data.get('wd', 0)
        if pass_id:
            item = db.session.query(Item).filter(Item.pass_id == pass_id, Item.lau_usId == data['token'].get_openid()).first()
            if item:
                lauser = db.session.query(User).filter(User.openid == data['token'].get_openid()).first()
                item_detaildict = {'item_name': item.item_name, 'pass_id': item.pass_id, 'item_type': item.item_type,
                                   'contacter': lauser.nickname,
                                'contacts': item.contacts, 'start_time': json.dumps(item.start_time, cls=DateEncoder),
                                'end_time': json.dumps(item.end_time, cls=DateEncoder), 'item_address': item.item_address,
                                'text_info':item.text_info, 'img_info': item.img_info, 'page_show': item.page_show, 'logic_del': item.logic_del}
                ord_objects = db.session.query(OrdObject).filter(OrdObject.itemId == item.item_id).all()
                '''字段：obj_id itemId obj_num obj_name minOrd_time startOrd_time ordable_sum residue'''
                ord_objectlist = [{'obj_id': ord_object.obj_id,'obj_num': ord_object.obj_num,
                                   'obj_name': ord_object.obj_name, 'minOrd_time': ord_object.minOrd_time,
                                   'startOrd_time': ord_object.ordable_sum, 'residue': ord_object.residue
                                   }for ord_object in ord_objects if ord_object.logic_del]
                info = {"errNum": 0, "errMsg": "success", 'data': {'item_detail': item_detaildict, 'ord_objects': ord_objectlist}}
                return jsonify(info)
            else:
                info = {"errNum": -1, "errMsg": 'wdError.'}
                return jsonify(info)
        else:
            info = {"errNum": -1, "errMsg": 'keyError.'}
            return jsonify(info)
    return decorated(request)


# 我的加入的列表
@iteminfo.route('/Myjoined', methods=['POST'])
def myjoined_itemlist():
    @token.checkbytoken
    def decorated(data):
        # 加入的项目列表对象
        itemlist = db.session.query(Item).filter(Item.item_id.in_(db.session.query(OrdObject.itemId).filter(OrdObject.obj_id.in_
                                                  (db.session.query(Orderinfo.objId).filter(Orderinfo.ordNum.in_
                                                                                                     (db.session.query(Order.ord_num).filter(Order.ord_usId == data['token'].get_openid())
                                                                                                      )))))).all()

        if itemlist:
            # item_todict = [{'item_name':item.item_name, 'pass_id': item.pass_id,'item_type': item.item_type,'logic_del':item.logic_del,
            #                 'overed':(item.end_time<datetime.datetime.now()), 'start_time': json.dumps(item.start_time, cls=DateEncoder),
            #                 'end_time': json.dumps(item.end_time, cls=DateEncoder)} for item in itemlist]

            # 返回项目的名称 口令 类型 是否过期 是否被逻辑删除（取消） 开始时间 结束时间 信息
            item_todict = [{'item_name': item.item_name, 'pass_id': item.pass_id, 'item_type': item.item_type, 'text_info': item.text_info,
                            'overed': (item.end_time<datetime.datetime.now()), 'start_time': json.dumps(item.start_time, cls=DateEncoder),
                            'end_time': json.dumps(item.end_time, cls=DateEncoder), 'address': item.item_address, 'logic_del': item.logic_del} for item in itemlist]
            info = { "errNum": 0, "errMsg": "success", 'data': item_todict}
            return jsonify(info)
        else:
            info = {"errNum": -1, "errMsg": "itemNull."}
            return jsonify(info)
    return decorated(request)

# 我加入的项目的详情
@iteminfo.route('/Myjoined/detail', methods=['POST'])
def myjoined_itemdetail():
    @token.checkbytoken
    def decorated(data):
        print(request.get_json())
        pass_id = data.get('wd', 0)
        if pass_id:
            myitem = db.session.query(Item).filter(Item.pass_id == pass_id).first()
            if myitem:
                lauser = db.session.query(User).filter(User.openid == data['token'].get_openid()).first()
                # 请求的项目的信息返回
                myitem_detaildict = {'item_name': myitem.item_name, 'pass_id': myitem.pass_id, 'item_type': myitem.item_type,
                                    'contacts': myitem.contacts, 'contacter': lauser.nickname,
                                     'start_time': [myitem.start_time.year, myitem.start_time.month, myitem.start_time.day, myitem.start_time.hour, myitem.start_time.minute] ,
                                    'end_time': [myitem.end_time.year, myitem.end_time.month, myitem.end_time.day, myitem.end_time.hour, myitem.end_time.minute],
                                     'item_address': myitem.item_address,
                                    'text_info':myitem.text_info, 'img_info': myitem.img_info, 'logic_del': myitem.logic_del,
                                    'lau_time':     [myitem.lau_time.year, myitem.lau_time.month, myitem.lau_time.day, myitem.lau_time.hour, myitem.lau_time.minute]}
                #我的订单详情表
                # my_orders = db.session.query(Orderinfo).filter(Orderinfo.ordNum.in_(db.session.query(Order.ord_num).filter(Order.ord_usId == data['token'].get_openid())))

                myorded_objects = db.session.query(OrdObject).filter(OrdObject.obj_id.in_
                                                      (db.session.query(Orderinfo.objId).filter(Orderinfo.ordNum.in_
                                                                                                         (db.session.query(Order.ord_num).filter(Order.ord_usId == data['token'].get_openid())
                                                                                                          ))), OrdObject.item == myitem).all()
                #本项目中我预定了的对象
                ord_objectlist = [{'obj_id': myorded_object.obj_id,'obj_num': myorded_object.obj_num,
                                   'obj_name': myorded_object.obj_name, 'minOrd_time': myorded_object.minOrd_time,
                                   'startOrd_time':  datetime_to_list(myorded_object.startOrd_time), 'residue': myorded_object.residue,
                                   'logic_del': myorded_object.logic_del
                                   }for myorded_object in myorded_objects]
                info = {'data':{'item': myitem_detaildict, 'my_obj': ord_objectlist}, "errNum": 0, "errMsg": "success"}
                db.session.close()
                return jsonify(info)
            else:
                db.session.close()
                info = {"errNum": -1, "errMsg": "itemError."}
                return jsonify(info)
        else:
            db.session.close()
            info = {"errNum": -1, "errMsg": 'keyError.'}
            return jsonify(info)
    return decorated(request)


# @iteminfo.route('/alteriteminfo/Myjoined', methods=['POST'])
# def alter_info():
#     @token.checkbytoken
#     def decorated(data):
#         openid = data['token'].get_openid()
#         del_obj_id = data.get('obj_id', 0)
#         if del_obj_id:
#
#         return decorated(request)

