import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import pytesseract
import matplotlib.pyplot as plt
import time
import re
import sys

import imutils
from imutils.perspective import four_point_transform

from sqlalchemy import create_engine
conn_string='oracle+cx_oracle://dzjc:dzjc@192.168.1.15:1521/orcl'
engine = create_engine(conn_string, echo=False)

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"




# 识别二维码程序
def QR_image(img):
    identification = []
    inforesout = pyzbar.decode(img)
    for dadada in inforesout:
        identification.append(dadada.data.decode("utf-8"))
#             print(dadada.data.decode("utf-8"))
    return identification

# 四边形矫正
def change_size(image):
    # 读取图片
    width1, height1 = image.shape[1], image.shape[0]
    # 转灰色
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 高斯滤波
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 自适应二值化方法
    blurred=cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,2)
#     blurred=cv2.copyMakeBorder(blurred,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))
    # 找到边框
    edged = cv2.Canny(blurred, 10, 100)
    # 找到矩阵
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None

    if len(cnts) > 0:
        # 将轮廓按大小降序排序
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # 对排序后的轮廓循环处理
        for c in cnts:
            # 获取近似的轮廓
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # 如果近似轮廓有四个顶点，那么就认为找到了图片
            if len(approx) == 4:
                docCnt = approx
                break
    newimage = image.copy()
    for i in docCnt:
        #circle函数为在图像上作图，新建了一个图像用来演示四角选取
        cv2.circle(newimage, (i[0][0],i[0][1]), 10, (255, 0, 0), -1)
        
    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))

    # 对灰度图应用二值化算法
    thresh = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
    paper = cv2.resize(paper, (width1, height1), cv2.INTER_LANCZOS4)
    paper = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("resoutlicence.jpg", paper)
    return paper


#  从上倒下分隔图片
def getImageHorizontalAndVerticalSum(image):
    # ImageThre = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ImageThre = image
    ret, ImageThre=cv2.threshold(ImageThre, 125,255, cv2.THRESH_BINARY_INV)
    rows, cols = ImageThre.shape
    horsum = []
    versum = []
    for i in range(cols):
        val = np.array(ImageThre[:, i]).sum()
        horsum.append(val)
    for i in range(rows):
        val = np.array(ImageThre[i, :]).sum()
        versum.append(val)
    return horsum,versum    

 
#这个函数我们最终需要找到一个区间表示字符的竖直分布情况
def getVerticalCharPosition(versum):
    result=[] #用来保存找到的结果：位置，区间大小
    i = 0
    while i< len(versum):
        if(versum[i] > 500):
            j=1 #代表这个区间的大小
            sumver = versum[i] #代表这整个区间的像素和是多少
            while(versum[i+j] > 500):
                sumver = sumver + versum[i + j]
                j = j + 1     
                if i+j == len(versum):
                    break
            if j > 60 and sumver > 4000: 
                result.append([i, j])
            i = i + j + 1 #跳过这整个不为0的区间，开始寻找下一个区间
        i = i + 1
    return result
 
def getHorizontalCharPosition(horsum):
    result = []  # 用来保存找到的结果：位置，区间大小
    i = 0 
    while  i < len(horsum):
        if(horsum[i] > 2000):
            result.append(i)
         #跳过这整个不为0的区间，开始寻找下一个区间
        i = i+1
    return min(result), max(result)


# 这个函数返回所有可能是字符的图片区域
def getCharImages(verticalCharPosition, image):
    weight = image.shape[1]
    charImages = []
    for v in verticalCharPosition:
        charImages.append(image[v[0]: v[0]+v[1], 0: weight])
    return charImages 

# 确定列表开始的地方
def get_start(lis):
    for index in range(len(lis)):
        pattern = re.compile('\d{6}')
        if pattern.search(lis[index]):
            ss = index
            return ss
    return 0

def main():
    # 参数1.选择图片的
    if len(sys.argv) == 1:
        print({"status": "400",
               "msg": "没有传入图片路径参数"})
        return  "没有传入图片路径参数"
    else:
        image = sys.argv[1] 
    
    if sys.argv[2] == '1':
        print({"msg": "数据存入数据库"})   
    else:
        print({"msg": "数据存入json"})



    img = cv2.imread(image, cv2.IMREAD_COLOR)
    message = QR_image(img)
    # 如果有识别到二维码并返回二维码的数据即可
    if message:
        if sys.argv[2]=="1":
            print("已经存在数据库了")
            # done_data.to_sql('xxx', con=engine, if_exists='append')
            # engine.close()
            return "已经存数据库了"

        else:
            print({"status": "200",
                "msg": "success",
                "data": message})
            return message

    image = change_size(img)  
    # 获取水平和垂直方向的图片分隔数据  
    horsum,versum = getImageHorizontalAndVerticalSum(image)
    # 获取垂直方向的分隔数据
    verticalCharPosition = getVerticalCharPosition(versum)
    # 分隔图片
    # 应该先做处理的
    catimg = getCharImages(verticalCharPosition, image)
    lis = []
    for i in range(len(catimg)):
        h = catimg[i].shape[0]
        horsumv, versumv = getImageHorizontalAndVerticalSum(catimg[i])
        s, e = getHorizontalCharPosition(horsumv)
        cv2.imwrite('%s.jpg'%(i), catimg[i][0: h, max(s-50,0): e+50])
        lis.append(''.join(pytesseract.image_to_string(catimg[i][0:h, max(s-50,0): e+50], lang="chi_sim").split()))
    start = get_start(lis)
    lis1 = lis[start:start+8]
    if len(lis1) > 5:
        if sys.argv[2]=="1":
            print("已经存在数据库了")
            # done_data.to_sql('xxx', con=engine, if_exists='append')
            # engine.close()
            return "已经存数据库了"

        else:
            print(
                {"status": "200",
                "msg": "success",
                "data": lis1})
            return lis1

    print({
            "status": "400",
            "msg": "failure",
            "data": "识别失败，请重新上传图片"})
    return({
            "status": "400",
            "msg": "failure",
            "data": "识别失败，请重新上传图片"})

if __name__ == "__main__":
    t2= time.time()
    img_url = r"F:/PYcode/Coding/ic/license/source_img/4.jpg"
    main()
    t3 = time.time()-t2
    print(t3)