from flask import Blueprint, jsonify, request
from methods import Token
from model.redis_models import *

collect_formId = Blueprint('collect_formId', __name__)
token = Token()

@collect_formId.route('/formId')
def get_formId():
    @token.checkbytoken
    def decorated(data):
        openid = data['token'].get_openid()
        formId = data.get('formId', None)
        red = Redis_db('formId')
        if formId:
            if red.set_formId(openid, formId):
                info = {"errNum": 0, 'errMsg': 'success'}
                return jsonify(info)
            else:
                info = {'errorNum': -1, 'errMsg': 'db Error.'}
                return jsonify(info)
        else:
            info = {'errorNum': -1, 'errMsg': 'form Error.'}
            return jsonify(info)
    return decorated(request)