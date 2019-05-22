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
        itemlist = db.session.query(Item).filter(
            Item.lau_usId == data['token'].get_openid()).all()
        if itemlist:
            '''item字段 ：item_id item_name pass_id lau_usId item_type
             contacts start_time end_time item_address text_info img_info page_show'''
            # item_todict = [{'item_name':item.item_name, 'pass_id': item.pass_id,'item_type': item.item_type,
            #                 'contacts': item.contacts, 'start_time': json.dumps(item.start_time, cls=DateEncoder),
            #                 'end_time': json.dumps(item.end_time, cls=DateEncoder), 'item_address': item.item_address,
            #                 'text_info':item.text_info, 'img_info': [], 'page_show': item.page_show}
            #                for item in itemlist]非详情页不需要这么多信息
            # 返回项目名称，项目口令 项目类型 是否过期 是否被逻辑删除（被用户取消）
            item_todict = [{'item_name': item.item_name,
                            'pass_id': item.pass_id,
                            'item_type': item.item_type,
                            'text_info': item.text_info,
                            'img_info': item.img_info,
                            'overed': (item.end_time < datetime.datetime.now()),
                            'logic_del': item.logic_del} for item in itemlist]
            info = {'data': item_todict, "errNum": 0, "errMsg": "success"}
            print(info)
            db.session.close()
            return jsonify(info)
        else:
            info = {"errNum": 0, "errMsg": "itemNull."}
            db.session.close()
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
            item = db.session.query(Item).filter(
                Item.pass_id == pass_id,
                Item.lau_usId == data['token'].get_openid()).first()
            if item:
                lauser = db.session.query(User).filter(
                    User.openid == data['token'].get_openid()).first()
                item_detaildict = {
                    'item_name': item.item_name,
                    'pass_id': item.pass_id,
                    'item_type': item.item_type,
                    'contacter': item.contacter if item.contacter else lauser.nickname,
                    'contacts': item.contacts,
                    'start_time': datetime_to_list(
                        item.start_time),
                    'end_time': datetime_to_list(
                        item.end_time),
                    'item_address': item.item_address,
                    'text_info': item.text_info,
                    'img_info': item.img_info,
                    'page_show': item.page_show,
                    'logic_del': item.logic_del}
                ord_objects = db.session.query(OrdObject).filter(
                    OrdObject.itemId == item.item_id).all()
                '''字段：obj_id itemId obj_num obj_name minOrd_time startOrd_time ordable_sum residue'''
                ord_objectlist = [
                    {
                        'obj_id': ord_object.obj_id,
                        'obj_num': ord_object.obj_num,
                        'obj_name': ord_object.obj_name,
                        'minOrd_time': ord_object.minOrd_time,
                        'startOrd_time': datetime_to_list(
                            ord_object.startOrd_time),
                        'ordable_sum': ord_object.ordable_sum,
                        'residue': ord_object.residue}for ord_object in ord_objects if ord_object.logic_del]
                info = {
                    "errNum": 0,
                    "errMsg": "success",
                    'data': {
                        'item_detail': item_detaildict,
                        'ord_objects': ord_objectlist}}
                db.session.close()

                return jsonify(info)
            else:
                db.session.close()

                info = {"errNum": -1, "errMsg": 'wdError.'}
                return jsonify(info)
        else:
            db.session.close()
            info = {"errNum": -1, "errMsg": 'keyError.'}
            return jsonify(info)
    return decorated(request)


# 我的加入的列表
@iteminfo.route('/Myjoined', methods=['POST'])
def myjoined_itemlist():
    @token.checkbytoken
    def decorated(data):
        # 加入的项目列表对象
        itemlist = db.session.query(Item).filter(
            Item.item_id.in_(
                db.session.query(
                    OrdObject.itemId).filter(
                    OrdObject.obj_id.in_(
                        db.session.query(
                            Orderinfo.objId).filter(
                            Orderinfo.ordNum.in_(
                                db.session.query(
                                    Order.ord_num).filter(
                                        Order.ord_usId == data['token'].get_openid()))))))).all()

        if itemlist:
            # item_todict = [{'item_name':item.item_name, 'pass_id': item.pass_id,'item_type': item.item_type,'logic_del':item.logic_del,
            #                 'overed':(item.end_time<datetime.datetime.now()), 'start_time': json.dumps(item.start_time, cls=DateEncoder),
            #                 'end_time': json.dumps(item.end_time, cls=DateEncoder), 'img_info': item.img_info} for item in itemlist]

            # 返回项目的名称 口令 类型 是否过期 是否被逻辑删除（取消） 开始时间 结束时间 信息
            item_todict = [{'item_name': item.item_name,
                            'pass_id': item.pass_id,
                            'item_type': item.item_type,
                            'text_info': item.text_info,
                            'img_info': item.img_info,
                            'overed': (item.end_time < datetime.datetime.now()),
                            'start_time': json.dumps(item.start_time,
                                                     cls=DateEncoder),
                            'end_time': json.dumps(item.end_time,
                                                   cls=DateEncoder),
                            'address': item.item_address,
                            'logic_del': item.logic_del} for item in itemlist]
            info = {"errNum": 0, "errMsg": "success", 'data': item_todict}
            db.session.close()
            return jsonify(info)
        else:
            db.session.close()
            info = {"errNum": 0, "errMsg": "itemNull."}
            return jsonify(info)
    return decorated(request)

# 我加入的项目的详情


@iteminfo.route('/Myjoined/detail', methods=['POST'])
def myjoined_itemdetail():
    @token.checkbytoken
    def decorated(data):
        pass_id = data.get('wd', 0)
        if pass_id:
            myitem = db.session.query(Item).filter(
                Item.pass_id == pass_id).first()
            if myitem:
                lauser = db.session.query(User).filter(
                    User.openid == data['token'].get_openid()).first()
                # 查询订单 查看加入动作 是否被取消 存放到项目相关的信息字段
                orders_cancel_del = db.session.query(
                    Order.cancel_del).filter(
                    Order.ord_itemId == myitem.item_id,
                    Order.ord_usId == data['token'].get_openid()).all()
                # 请求的项目的信息返回
                myitem_detaildict = {
                    'item_name': myitem.item_name,
                    'pass_id': myitem.pass_id,
                    'item_type': myitem.item_type,
                    'contacts': myitem.contacts,
                    'contacter': myitem.contacter if myitem.contacter else lauser.nickname,
                    'start_time': [
                        myitem.start_time.year,
                        myitem.start_time.month,
                        myitem.start_time.day,
                        myitem.start_time.hour,
                        myitem.start_time.minute],
                    'end_time': [
                        myitem.end_time.year,
                        myitem.end_time.month,
                        myitem.end_time.day,
                        myitem.end_time.hour,
                        myitem.end_time.minute],
                    'item_address': myitem.item_address,
                    'cancel_status': 1 if [
                        i for i in orders_cancel_del if i[0] != 0] else 0,
                    'text_info': myitem.text_info,
                    'img_info': myitem.img_info,
                    'logic_del': myitem.logic_del,
                    'lau_time': [
                        myitem.lau_time.year,
                        myitem.lau_time.month,
                        myitem.lau_time.day,
                        myitem.lau_time.hour,
                        myitem.lau_time.minute]}

                # 有bug 一个用户可能预定了多次同一个预定对象 有多个队列号
                myorded_objects = db.session.query(
                    OrdObject,
                    Orderinfo.queue_num,
                    Order.cancel_del).filter(
                    OrdObject.obj_id.in_(
                        db.session.query(
                            Orderinfo.objId).filter(
                            Orderinfo.ordNum.in_(
                                db.session.query(
                                    Order.ord_num).filter(
                                    Order.ord_usId == data['token'].get_openid())))),
                    OrdObject.item == myitem,
                    Orderinfo.objId == OrdObject.obj_id,
                    Order.ord_num == Orderinfo.ordNum).all()

                # 本项目中我预定了的对象
                ord_objectlist = [
                    {
                        'obj_id': myorded_object[0].obj_id,
                        'obj_num': myorded_object[0].obj_num,
                        'obj_name': myorded_object[0].obj_name,
                        'minOrd_time': myorded_object[0].minOrd_time,
                        'startOrd_time': datetime_to_list(
                            myorded_object[0].startOrd_time),
                        'residue': myorded_object[0].residue,
                        'logic_del': myorded_object[0].logic_del,
                        'queue_num': myorded_object[1],
                        'cancel_status': myorded_object[2],
                    }for myorded_object in myorded_objects]
                info = {
                    'data': {
                        'item': myitem_detaildict,
                        'my_obj': ord_objectlist},
                    "errNum": 0,
                    "errMsg": "success"}
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


# 用户取消发起或者改变首页状态 逻辑: 取消发起：找出项目表项目 找对象表对象 逻辑删除， 改变首页状态 找项目表page_show 改成指定值
@iteminfo.route('/alteriteminfo/Mylaunched', methods=['POST'])
def alter_launchinfo():
    @token.checkbytoken
    def decorated(data):
        openid = data['token'].get_openid()
        pass_id = data.get('wd', 0)
        page_show = data.get('page_show_status', -1)
        logic_del = data.get('logic_del_status', -1)
        item = db.session.query(Item).filter(
            Item.pass_id == pass_id,
            Item.lau_usId == openid).first()
        if item:
            if page_show != -1:
                item.page_show = 1 if page_show else 0
            elif logic_del != -1:
                item.logic_del = 1 if logic_del else 0
                # 取消动作 不能重新发起需要重新填写表单
                if logic_del == 0:
                    objs = db.session.query(OrdObject).filter(
                        OrdObject.itemId == item.item_id)
                    for obj in objs:
                        obj.logic_del = 0
                        db.session.add(obj)
            else:
                info = {"errNum": -1, "errMsg": 'unknow Opera'}
                db.session.close()
                return jsonify(info)

            db.session.add(item)
            db.session.commit()
            db.session.close()
            info = {
                "errNum": 0,
                "errMsg": 'success',
                'data': 'page_show_changed'}
            return jsonify(info)
        else:
            db.session.close()
            info = {"errNum": -1, "errMsg": "itemError."}
            return jsonify(info)
    return decorated(request)


# 用户取消加入 逻辑：找到项目对应的所有订单 cancel_del 全部改成 0 全部取消
@iteminfo.route('/alteriteminfo/Myjoined', methods=['POST'])
def alter_joininfo():
    @token.checkbytoken
    def decorated(data):
        openid = data['token'].get_openid()
        pass_id = data.get('wd', 0)
        # 找到要取消加入的项目
        item = db.session.query(Item).filter(
            Item.pass_id == pass_id, Item.logic_del == 1).first()
        if item:
            # 找到要取消 加入项目 和 该用户相关的对应的 订单
            alter_orders = db.session.query(Order).filter(
                Order.ord_itemId == item.item_id, Order.ord_usId == openid)
            if alter_orders:
                # 修改相关字段 cancel_del
                for alter_order in alter_orders:
                    alter_order.cancel_del = 0
                    db.session.add(alter_order)
                # db add db commit
                db.session.commit()
                db.session.close()
                info = {"errNum": 0, "errMsg": "success"}
                return jsonify(info)
            else:

                info = {"errNum": -1, "errMsg": "userError."}
                return jsonify(info)
        else:
            info = {"errNum": -1, "errMsg": "itemError."}
            return jsonify(info)
    return decorated(request)
