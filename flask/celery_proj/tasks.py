from __future__ import absolute_import
import requests
from celery_proj.celery import app as ap
import sys
sys.path.append("..")
from model.redis_models import Redis_db
from model.ord_models import *
import datetime

template_id = 'WJuAWZ1DGHzjcOk0W2BevWkZdORxITBNZE5gUfHEr9M'
app_id = 'wx64118b44bbd3bfa3'
secret_key = '9ca7dc56b74663931643555302ef90e5'


def get_access_token(app_id=app_id, secret_key=secret_key):
    ''' 获取微信access_token'''
    try:
        payload = {
            'grant_type': 'client_credential',
            'appid': app_id,
            'secret': secret_key
        }
        req = requests.get(
            'https://api.weixin.qq.com/cgi-bin/token',
            params=payload,
            timeout=3,
            verify=False)
        access_token = req.json().get('access_token', "")
        print('access_token', access_token)
        return access_token
    except Exception as e:
        print(e)


def push(
        openid,
        formId,
        item_info: dict,
        access_token,
        template_id=template_id):
    '''推送消息'''
    data = {
        "touser": openid,
        "template_id": template_id,
        "form_id": formId,
        'page': 'pages\person\myjoinedlist\myjoineditem_detail\myjoineditem_detail?wd={}'.format(
            item_info.get(
                'item_pass_id',
                '未知')),
        "data": {
            'keyword1': {
                'value': item_info.get(
                    'item_name',
                    '未知')},
            'keyword2': {
                'value': item_info.get(
                    'item_address',
                    '未知')},
            'keyword3': {
                'value': item_info.get(
                    'item_start_time',
                    '未知')}},
        "emphasis_keyword": ''}
    push_url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={}'.format(
        access_token)
    result = requests.post(push_url, json=data, timeout=3, verify=False)
    return result


@ap.task
def pullMsg(delta=60):
    '''推送消息'''
    access_token = get_access_token()
    now = datetime.datetime.now()
    timedel = datetime.datetime.now() + datetime.timedelta(minutes=delta)
    # 搜索所有快要开始的活动
    objlist = db.session.query(OrdObject.obj_id).filter(
        OrdObject.startOrd_time <= timedel,
        OrdObject.startOrd_time >= now)
    # 搜索相关订单
    ordlist = db.session.query(Orderinfo.ordNum).filter(
        Orderinfo.objId.in_(objlist)
    )
    # 搜索所有符合的用户，预定信息，项目名称，地址， 并且逐个推送
    # all (1, 'jhon', 'xixixi', 'bbbUI0egBJY1zhBYw2KhdUfwVJJE', datetime.datetime(2019, 5, 5, 14, 0))
    result = db.session.query(
        Item.item_id,
        Item.item_name,
        Item.item_address,
        Item.pass_id,
        Order.ord_usId,
        db.func.min(
            OrdObject.startOrd_time)).join(
        Orderinfo,
        Order.ord_num == Orderinfo.ordNum).outerjoin(OrdObject).filter(
                OrdObject.obj_id == Orderinfo.objId,
                OrdObject.startOrd_time <= timedel,
                OrdObject.startOrd_time <= now).group_by(
                    Item.item_id,
        Order.ord_usId).all()
    # 按状态推送 已推送的不推送
    status_db = Redis_db('pushMsg_status')
    formId_db = Redis_db('formId')
    if result:
        for i in result:
            item_id, openid = i[0], i[4]
            # 检查是否已推送
            response = status_db.check_pushMsg_status(item_id, openid)
            if response:
                # 已推送 下个
                continue
            else:

                # 未推送
                # 记录状态为已推送 假设未推送成功也最少24小时后再试
                response = status_db.set_pushMsg_status(item_id, openid)
                formId = formId_db.get_formId(openid)
                if formId:
                    # 推送 无法推送的情况，需要 改进redis过期时间
                    item_info = {
                        'item_name': i[1],
                        'item_address': i[2],
                        'item_pass_id': i[3],
                        'item_start_time': '{0}.{1}.{2} {3}:{4}'.format(
                            i[5].year,
                            i[5].month,
                            i[5].day,
                            i[5].hour,
                            i[5].minute)}
                    return push(openid, formId, item_info, access_token)
                else:
                    # 无法推送
                    return 'without formId!'
    else:
        return 'NO RESULT!'