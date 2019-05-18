import os
import cv2
from werkzeug.utils import secure_filename

filename = '2.png'
basepath = os.path.dirname(__file__)
upload_path = os.path.join(basepath, 'static/itemimg', secure_filename(filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
#
# with open(upload_path, 'rb') as f:
#     a = f.read()
newfilename = '88.png'
# os.rename(os.path.join(basepath, 'static/itemimg', secure_filename(filename)),
#                           os.path.join(basepath, 'static/itemimg', newfilename))
# print(a)

img = cv2.imread('./static/itemimg/78.png')
print(img)
cv2.imwrite('./static/itemimg/111.jpg',  img, [int(cv2.IMWRITE_JPEG_QUALITY),70])
