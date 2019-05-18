'''用户登录相关的api'''

from flask import Blueprint, json, request, jsonify
from ord_models import *
from methods import get_user, Token, WXBizDataCrypt, try_db_commit, appid, secret

#创建蓝图
login = Blueprint('login', __name__)


#登录 返回token数据 更新token数据
@login.route('/newuser', methods=['POST'])
def sign_in():
    json_data = request.get_json()
    js_code = json_data['code']
    print(js_code)
    user_session = get_user(js_code)  # 字典类型
    print(user_session)
    session_key = user_session.get('session_key', 0)
    openid = user_session.get('openid', 0)
    #0 请求成功
    if session_key and openid:
        tokenobj = Token(openid=openid, session_key=session_key)
        token = tokenobj.set_pawd()
        if not db.session.query(User).filter(User.openid==openid).first():
            #这是一个新用户
            newuser = User(openid=openid)
            db.session.add(newuser)
            db.session.commit()

        info = {"errNum": 0, "errMsg": "success", 'User_token': token}
        return jsonify(info)
    #请求失败
    else:
        info = {"errNum": -1, "errMsg": "condeError.", 'WxerrMsg': user_session["errmsg"]}
        return jsonify(info)

token = Token()

@login.route('/user/update', methods=['POST'])
def update_userinfo():
    #用户修改个人信息
    @token.checkbytoken
    def decorated(data):
        openid = data['token'].get_openid()
        user = db.session.query(User).filter(User.openid == openid).first()
        if user:
            try:
                address = data['address']
                phone = data['phone']
            except:
                info = {"errNum": -1, "errMsg": "keysError."}
                return jsonify(info)
            if address:
                user.address = address
            if phone:
                user.phone = phone
            return try_db_commit(user)
        else:
            info = {"errNum": -1, "errMsg": "userinexistError."}
            return jsonify(info)
    return decorated(request)


@login.route('/userinfo', methods=['POST'])
def upload_userinfo():
    # 更新用户名和头像
    @token.checkbytoken
    def decorated(data):
        try:
            encryptedData = data['encryptedData']
            iv = data['iv']
        except:
            info = {"errNum": -1, "errMsg": "keysError."}
            return jsonify(info)
        # sessionKey用Redis数据库
        # 密文 解密得到对象
        pc = WXBizDataCrypt(appid, token.get_session_key())
        # 得到字典对象的用户信息
        userinfo = pc.decrypt(encryptedData, iv)
        #item = Item.query.filter_by(pass_id=pass_id).first()
        '''存在bug 一个用户可以用截获的他人的表单 验证自己的token 然后修改他人的新型'''
        user = db.session.query(User).filter_by(openid=userinfo['openId']).first()
        if user:
            user.nickname = userinfo['nickName']  # 存在问题:多用户在高并发的情况下对同一数据进行操作可能会返回错误的队号
            user.avatarurl = userinfo['avatarUrl']
            return try_db_commit(user)
        else:
            info = {"errNum": -1, 'errMsg': "withoutloginopra."}
            return jsonify(info)
    return decorated(request)

