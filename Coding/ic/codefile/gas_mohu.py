# -*- coding:utf-8 -*-

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 文件路径
path = "./116.png"
# 载入一张图片，参数cv.CV_LOAD_IMAGE_GRAYSCALE为打开为灰度图
lwpImg = cv.imread(path, 0)
# 创建图像空间，参数为size, depth, channels，这里设置的是图片等高宽30个像素的一个区域，8位，灰度图
box_lwpImg = cv.imwrite((30, 576), 8, 1)

# 创建窗口
cv.NamedWindow('test1', cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("box_test1", cv.CV_WINDOW_AUTOSIZE)

# 设置ROI区域，即感兴趣区域，参数为x, y, width, heigh
cv.SetImageROI(lwpImg, (390, 0, 30, 576)) 
# 提取ROI，从lwpImg图片的感兴趣区域到box_lwpImg
cv.Copy(lwpImg, box_lwpImg)

# 对box区域进行循环提取像素值存到列表pixel_list中
pixel_list = []
for i in range(576): # 576为box的高
    for j in range(30): # 30为box的宽
        x = box_lwpImg[i, j]
        pixel_list.append(x)

# 提取的像素值转为int整型赋给一维数组pixel_list_np_1
pixel_list_np_1 = np.array(pixel_list, dtype=int)
# 转为576*30的二位数组，即按图片box排列
pixel_list_np_2 = np.array(pixel_list_np_1).reshape(576, 30)
# 行求和，得到576个值，即每行的像素信息
pixel_sum = np.sum(pixel_list_np_2, axis=1)

# 取消设置
cv.ResetImageROI(lwpImg)

# 画目标区域
lwpImg = cv.Rectangle(lwpImg, (390, 0), (425, 576), (0, 255, 0), 2)
# 显示图像
cv.ShowImage('test1', lwpImg)
# 查看列表list长度，以确定像素值提取准确
list_length = len(pixel_list)
print(list_length)

# 查看数组维度，shape验证
print(pixel_list_np_1.ndim)
print(pixel_list_np_1.shape)
print(pixel_list_np_1)

print(pixel_list_np_2.ndim)
print(pixel_list_np_2.shape)
print(pixel_list_np_2)

print(pixel_sum)

# 画条形图
plt.figure(1)
width = 1
for i in range(len(pixel_sum)):
    plt.figure(1)
    plt.bar(i, pixel_sum[i], width)
plt.xlabel("X")
plt.ylabel("pixel_sum")
plt.show()

# 按ESC退出，按s保存图片
k = cv.WaitKey(0)
if k == 27:                 # wait for ESC key to exit
    cv.DestroyAllWindows()
elif k == ord('s'):         # wait for 's' key to save and exit
    cv.WriteFrame('copy_test.png', lwpImg)
    cv.DestroyAllWindows()
