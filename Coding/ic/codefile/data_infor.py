import cv2
import numpy as np
import os
from sys import argv
import time


def data_enhancement(img):
    # opencv 读取图片
    img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    # 设置前后背景色
    type(img)
    mask = np.zeros(img.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    # 获得要分别的矩形大小
    image_shape = img.shape
    rect = (20,20,image_shape[1]-20,image_shape[0]-20)
    # 前后背景颜色分离
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    # 阀值处理
    ret, thresh=cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY),127, 255, cv2.THRESH_BINARY)
    # 找到边
    image, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 找到满足的矩形
    for cnt in contours:
        # cv2.rectangle(img, (x, y), (x+w, y+h),(0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(cnt)
        if h < 200:
            continue
        #£ind bounding box coordinates
        else:
            epsilon = 0.01*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            # 矩形的四个顶点的数据,从三维转二维
            approx_n_shape = np.reshape(approx,(-1,approx.shape[-1])).astype(np.float32)  
            # image_shape  
            canvas = np.float32([[0, 0],[0, image_shape[0]],[image_shape[1], image_shape[0]],[image_shape[1], 0]])
            # 开始translate
            M = cv2.getPerspectiveTransform(approx_n_shape, canvas)
            result = cv2.warpPerspective(img, M, (0, 0))
            # result = cv2.resize(result,(600,400))          
            cv2.imwrite("f:\\PYcode\\Coding\\ic\\result_ti.jpg", result)

if __name__ == "__main__":
    img_path  = "f:\\PYcode\\Coding\\ic\\ti.jpg"
    # t1 = time.time()
    data_enhancement(img_path)
    # t2 = time.time()
    # print(t2-t1) # 1.389s



