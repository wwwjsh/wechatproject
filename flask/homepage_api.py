'''首页要调用的api'''

from flask import Blueprint, json, jsonify, request
from ord_models import *
import datetime
homepage = Blueprint('homepage', __name__)


@homepage.route('/items', methods=['POST'])
def get_items():
    itemslist = db.session.query(Item).filter(
        Item.logic_del != 0,
        Item.end_time >= datetime.datetime.now(),
        Item.page_show != 0)
    if itemslist:
        doing_items = [
            {
                'name': item.item_name,
                'pass_id': item.pass_id,
                'type': item.item_type,
                'text_info': item.text_info,
                'img_info': item.img_info} for item in itemslist.filter(
                Item.start_time <= datetime.datetime.now()).order_by(
                Item.start_time).all()]
        willbe_items = [
            {
                'name': item.item_name,
                'pass_id': item.pass_id,
                'type': item.item_type,
                'text_info': item.text_info,
                'img_info': item.img_info} for item in itemslist.filter(
                Item.start_time > datetime.datetime.now()).order_by(
                Item.start_time).all()]
        db.session.close()
        info = {
            'data': {
                'doing_items': doing_items,
                'willbe_items': willbe_items},
            "errNum": 0,
            "errMsg": "success"}
        return jsonify(info)
    else:
        db.session.close()
        info = {"errNum": -1, 'errMsg': 'itemsError.'}
        return jsonify(info)
