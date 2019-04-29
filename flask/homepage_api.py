'''首页要调用的api'''

from flask import Blueprint, json, jsonify, request
from ord_models import *
from methods import DateEncoder
import datetime
homepage = Blueprint('homepage', __name__)



@homepage.route('/items', methods=['POST'])
def get_items():
    itemslist = db.session.query(Item).filter(Item.logic_del != 0,
                                              Item.end_time >= datetime.datetime.now(),
                                              Item.page_show != 0).all()
    if itemslist:
        items_todict = [{'item_name': item.item_name, 'pass_id': item.pass_id, 'item_type': item.item_type,
                        'start_time': json.dumps(item.start_time, cls=DateEncoder), 'end_time': json.dumps(item.end_time, cls=DateEncoder)}
                        for item in itemslist]
        info = {'data': items_todict,"errNum": 0, "errMsg": "success"}
        return jsonify(info)
    else:
        info = {"errNum": -1, 'errMsg': 'itemsError.'}
        return jsonify(info)

