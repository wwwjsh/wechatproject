'''用户发起项目活动调用api'''

from flask import Blueprint, json, request, jsonify
from ord_models import *
import datetime
import os
import cv2
from methods import generate_random_str, Token, try_db_commit
from werkzeug.utils import secure_filename

# 创建蓝图
launch = Blueprint('launch', __name__)
token = Token()

# 用户发起活动
@launch.route('/launchActivity', methods=['POST'])
def lau_item():
    # json.loads(request.values.get("txt3"))
    # items表添加元素
    @token.checkbytoken
    def decorated(data):

        lau_usId = data['token'].get_openid()
        item_name = data['data']["item_name"]
        pass_id = generate_random_str(5)
        item_type = data['data']["item_type"]
        contacts = data['data']["contacts"]
        start_time = data['data']["start_time"]
        end_time = data['data']["end_time"]
        item_address = data['data']["item_address"]
        text_info = data['data']["text_info"]
        ord_objects = data['data']["ord_objects"]
        '''ord_objects:[{obj_num:int(3),obj_name:varchar(15),minOrd_time:int单位分钟,ordable_sum:预定类型为1 int(3) }]'''
        try:
            objlist = [] # 预定对象列表
            newItem = Item(lau_usId=lau_usId, item_name=item_name, pass_id=pass_id, item_type=item_type, contacts=contacts,
                       start_time=start_time[0], end_time=end_time[-1], item_address=item_address, text_info=text_info)
            # try_db_commit(newItem)
            db.session.add(newItem)
            db.session.flush()
                # print([start_time,end_time])
            for i in range(len(start_time)):
                a_start = start_time[i]
                a_end = end_time[i]
                for object in ord_objects:
                    # 遍历所有预定对象，例如五张桌子，遍历每张桌子
                    time = datetime.datetime.strptime(a_start, '%Y-%m-%d %H:%M')
                    end = datetime.datetime.strptime(a_end, '%Y-%m-%d %H:%M')
                    print(time,end)
                    while time < end:
                        # 切割小时间段
                        newObj = OrdObject(itemId=newItem.item_id, obj_num=object["obj_num"], obj_name=object["obj_name"],
                                           minOrd_time=object["minOrd_time"], startOrd_time=str(time), ordable_sum=object["ordable_sum"], residue=object["ordable_sum"])
                        objlist.append(newObj)
                        time = time + datetime.timedelta(minutes=object["minOrd_time"])
                    # ord_objects: [{obj_num: int(3), obj_name: varchar(15), minOrd_time: time, ordable_sum: int(3)}]}
            try:
                db.session.add_all(objlist)
                db.session.commit()
                # print(type(objlist))
                info = {"errNum": 0, "errMsg": "success", "pass_id": pass_id}
                return jsonify(info)
            except:
                info = {"errNum": -1, 'errMsg': "objError!"}
                return jsonify(info)
        except:
            info = {"errNum": -1, 'errMsg': "itemError!"}
            return jsonify(info)

    return decorated(request)


# 设置允许的文件格式
ALLOWED_EXTENSIONS = ['png', 'jpg', 'JPG', 'PNG', 'bmp']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@launch.route('/launchActivity/uploadimg', methods=['POST'])
def upload_itemimg():
    # 上传项目图片详情
    # file = request.files['file']
    # print(file)
    # basepath = os.path.dirname(__file__)  # 当前文件所在路径
    # #
    # upload_path = os.path.join(basepath, 'static/itemimg', secure_filename(file.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    # print(upload_path)
    # # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    # file.save(upload_path)
    # print(type(json.loads(request.values.get('formData'))))
    # print(request.get_json())
    @token.checkbytoken
    def decorated(data):
        item = db.session.query(Item).filter(Item.pass_id == data.get('wd', 0),
                                             Item.lau_usId == data['token'].get_openid()).first()
        if item:
            file = request.files['file']
            #获取二进制数据
            if not (file and allowed_file(file.filename)):
                info = {"errNum": -1, "errMsg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp", 'file.filename':file.filename}
                return jsonify(info)
            else:
                try:
                    basepath = os.path.dirname(__file__)  # 当前文件所在路径
                    upload_path = os.path.join(basepath, 'static/itemimg', secure_filename(file.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                    # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
                    file.save(upload_path)

                    # 使用Opencv转换一下图片格式和名称 转换成jpg
                    img = cv2.imread(upload_path)
                    filename = generate_random_str(12) + '.jpg'# 十二位字符串
                    cv2.imwrite(os.path.join(basepath, 'static/itemimg', filename), img, [int(cv2.IMWRITE_JPEG_QUALITY),70])
                    print(img)
                    item.img_info = filename
                    try_db_commit(item)
                    info = {"errNum": 0, "errMsg": "success"}
                    return jsonify(info)
                except:
                    info = {"errNum": -1, "errMsg": "serverError."}
                    return jsonify(info)
        else:
            info = {"errNum": -1, "errMsg": "itemError."}
            return jsonify(info)
    return decorated(json.loads(request.values.get('formData')))


