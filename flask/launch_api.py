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
def date_iterator(start_date, end_date):
    '''日期列表迭代器 存放每一个时间段里面的迭代器对象'''
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    if start_date > end_date:
        raise Exception('start_date bigger than end_date')
    date = start_date
    while date <= end_date:
        yield date
        date = date + datetime.timedelta(days=1)

def get_times_list(start_time, end_time, minOrd_time):
    '''生成一个对象 的一个时间段的时间列表'''
    start = datetime.datetime.strptime(start_time, '%H:%M')
    end = datetime.datetime.strptime(end_time, '%H:%M')
    if start > end:
        raise Exception('start_date bigger than end_date')
    timelist = []
    time = start
    while time < end:
        timelist.append(time)
        time = time + datetime.timedelta(minutes=int(minOrd_time))
    return timelist

def get_start_end(timetable):
    '''获取时间表的开始时间， 结束时间 作为该项目字段名'''
    min_datetime = datetime.datetime.strptime(timetable[0]['start_date']+' '+timetable[0]['start_time'], '%Y-%m-%d %H:%M')
    max_datetime = datetime.datetime.strptime(timetable[0]['end_date']+' '+timetable[0]['end_time'], '%Y-%m-%d %H:%M')
    for i in timetable:
        start = datetime.datetime.strptime(i['start_date'] + ' ' + i['start_time'], '%Y-%m-%d %H:%M')
        end = datetime.datetime.strptime(i['end_date'] + ' ' + i['end_time'], '%Y-%m-%d %H:%M')
        if start < min_datetime:
            min_datetime = start
        if end > max_datetime:
            max_datetime = end
    return (min_datetime, max_datetime)

# 用户发起活动
@launch.route('/launchActivity', methods=['POST'])
def lau_item():
    '''发起活动 相关函数参考some/test.py'''
    # json.loads(request.values.get("txt3"))
    # items表添加元素
    @token.checkbytoken
    def decorated(data):
        lau_usId = data['token'].get_openid()
        item_name = data['data'].get("item_name", '')
        pass_id = generate_random_str(5)
        item_type = data['data'].get("item_type", '2')
        contacts = data['data'].get("contacts", 0)
        contacter = data['data'].get("contacter", 0)
        timetable = data['data'].get("timetable", [])
        item_address = data['data'].get("address", '')
        text_info = data['data'].get("text_info", '')
        ord_objects = data['data'].get("objs", '')
        page_show = data['data'].get("objs", 1)
        '''ord_objects:[{obj_num:int(3),obj_name:varchar(15),minOrd_time:int单位分钟,ordable_sum:预定类型为1 int(3) }]'''
        '''time:[{ start_date: '2012-05-08', end_date: '2012-05-10', start_time: '14:00', end_time: '16:00' }]'''
        # 非空验证
        if (item_name and item_address and text_info and ord_objects and contacts and timetable):
            # 生成日期列表迭代器dateIterator 迭代之后的结果date:[['2012-05-08', '2012-05-09', '2012-05-10']] 一项表示一个日期区间的切分结果
            dateIterator = []
            for i in timetable:
                dateIterator.append(date_iterator(i['start_date'], i['end_date']))

            '''遍历寻找最预先的日期 和最终日期'''
            start_time, end_time = get_start_end(timetable)

            # 设定项目的开始时间和结束时间 数据库新建项目
            print(db.session.query(Item).filter(Item.pass_id == pass_id))
            # while db.session.query(Item).filter(Item.pass_id == pass_id).first():
            #     # 防止pass_id重复
            #     pass_id = generate_random_str(5)
            try:
                new_item = Item(lau_usId=lau_usId, item_name=item_name, pass_id=pass_id, item_type=str(item_type), contacts=contacts,
                                start_time=start_time, end_time=end_time, item_address=item_address, text_info=text_info, contacter=contacter,
                                page_show=page_show)

                db.session.add(new_item)
                db.session.flush()
                # 根据每个对象的最小预定时间 划分time中每个时间段对应的时间生成时间关系矩阵
                # 根据预定对象信息生成 时间列表  timelist = [[[14；00, 15:00],[根据第一个可预订对象， time第二个时间段切分的开始时间],...],[第二个可预订对象根据若干个time时间段的切分...]]
                timelist = []
                for obj in ord_objects:
                    obj_time = []
                    for i in timetable:
                        obj_time.append(get_times_list(i['start_time'], i['end_time'], obj['minOrd_time']))
                    timelist.append(obj_time)
                try:
                    # print(timelist)
                    # print(dateIterator)
                    # 生成根据多个开始时间段, 原来的obj信息，生成预定对象存入数据库
                    for i in range(len(timetable)):
                        for date in dateIterator[i]: # 遍历第i个时间段包含的日期
                            for obj_index in range(len(ord_objects)):
                                for time in timelist[obj_index][i]:
                                    startOrd_time = date + datetime.timedelta(hours=time.hour, minutes=time.minute)
                                    new_obj = OrdObject(itemId=new_item.item_id, obj_num=int(ord_objects[obj_index]["obj_num"]), obj_name=ord_objects[obj_index]["obj_name"],
                                                        minOrd_time=int(ord_objects[obj_index]["minOrd_time"]), startOrd_time=str(startOrd_time),
                                                        ordable_sum=int(ord_objects[obj_index]["ordable_sum"]), residue=int(ord_objects[obj_index]["ordable_sum"]))
                                db.session.add(new_obj)
                        db.session.commit()
                        db.session.close()
                        info = {"errNum": 0, "errMsg": "success", "pass_id": pass_id}
                        return jsonify(info)
                except:
                    db.session.rollback()
                    db.session.close()
                    info = {"errNum": -1, 'errMsg': "objError!"}
                    return jsonify(info)
            except:
                db.session.close()
                info = {"errNum": -1, 'errMsg': "itemError!"}
                return jsonify(info)
        else:
            info = {"errNum": -1, 'errMsg': "formError!"}
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
    # 构造标准data
    res_data = {'token': request.values.get('token'), 'wd': request.values.get('wd')}
    print(res_data)
    @token.checkbytoken
    def decorated(data):
        item = db.session.query(Item).filter(Item.pass_id == data.get('wd', 0),
                                             Item.lau_usId == data['token'].get_openid()).first()
        if item:
            file = request.files['file']
            #获取二进制数据
            if not (file and allowed_file(file.filename)):
                info = {"errNum": -1, "errMsg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"}
                return jsonify(info)
            else:
                try:
                    basepath = os.path.dirname(__file__)  # 当前文件所在路径
                    upload_path = os.path.join(basepath, 'static/itemimg', secure_filename(file.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                    # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
                    file.save(upload_path)
                    # with open(upload_path, 'rb') as f:
                    #     a = f.read()
                    # # 使用Opencv转换一下图片格式和名称 转换成jpg
                    # img = cv2.imread(upload_path)
                    # # filename = generate_random_str(12) + '.jpg'# 十二位字符串
                    # # cv2.imwrite(os.path.join(basepath, 'static/itemimg', filename), img, [int(cv2.IMWRITE_JPEG_QUALITY),70])
                    # print(img)
                    newfilename = generate_random_str(12) + '.jpg'
                    os.rename(os.path.join(basepath, 'static/itemimg', secure_filename(file.filename)),
                              os.path.join(basepath, 'static/itemimg', newfilename))
                    # 使用Opencv转换一下图片格式和名称 转换成jpg
                    img = cv2.imread('./static/itemimg/' + newfilename)
                    print(img)
                    # print(type(img)) img是none
                    cv2.imwrite('./static/itemimg/' + newfilename, img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                    # item.img_info = newfilename + ".jpg"
                    item.img_info = newfilename
                    # try_db_commit(item)
                    db.session.add(item)
                    db.session.commit()
                    info = {"errNum": 0, "errMsg": "success"}
                    return jsonify(info)
                except:
                    db.session.close()
                    info = {"errNum": -1, "errMsg": "serverError."}
                    return jsonify(info)
        else:
            db.session.close()
            info = {"errNum": -1, "errMsg": "itemError."}
            return jsonify(info)
    return decorated(res_data)



