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


#  从上倒下分隔图片
def getImageVerticalSum(image):
    # ImageThre = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ImageThre = image
    ret, ImageThre=cv2.threshold(ImageThre, 125,255, cv2.THRESH_BINARY_INV)
    rows, cols = ImageThre.shape[:2]
    versum = []
    for i in range(rows):
        val = np.array(ImageThre[i, :]).sum()
        versum.append(val)
    return versum  

#  从左倒右分隔图片
def getImageHorizontal(image):
    # ImageThre = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ImageThre = image
    ret, ImageThre=cv2.threshold(ImageThre, 125,255, cv2.THRESH_BINARY_INV)
    rows, cols = ImageThre.shape[:2]
    horsum = []
    for i in range(cols):
        val = np.array(ImageThre[:, i]).sum()
        horsum.append(val)
#     print(horsum)
    return horsum


#这个函数我们最终需要找到一个区间表示字符的水平分布情况
def getHorizontalCharPosition(horsum):
    result = []  # 用来保存找到的结果：位置，区间大小
    i = 0
    while i < len(horsum):
        if(horsum[i]!=0):
            j=1 #代表这个区间的大小
            sumhor = horsum[i] #代表这整个区间的像素和是多少
            while(i+j < len(horsum)):
                sumhor = sumhor + horsum[i+j]
                j=j+1
            if j > 10 and sumhor > 100:
                result.append([i,j])
            i=i+j+1 #跳过这整个不为0的区间，开始寻找下一个区间
        i=i+1
    return result

horimg = cv2.imread("2.jpg")
shorsum = getImageHorizontal(horimg)
horPosition = getHorizontalCharPosition(horsum)