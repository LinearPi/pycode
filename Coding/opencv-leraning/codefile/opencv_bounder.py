import cv2
import numpy as np
import matplotlib.pyplot as plt

# # 1.显示图片
# img = cv2.imread("8.jpg", 0)
# img.shape  #（高，宽，通道数）
# img.size
# img.
# cv2.imshow("img",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # plt显示图片
# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([]) 
# # to hide tick values on X and Y axis
# plt.plot([200,300,400],[100,200,300],'c', linewidth=5)
# plt.show()

# # 2.读取摄像头的数据
# cap = cv2.VideoCapture(1)
# # video
# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
# # end video

# while True:
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # video
#     out.write(frame)
#     # endviedo
    
#     cv2.imshow("frame", frame)
#     cv2.imshow("gray", gray)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# out.release()
# cv2.destroyAllWindows()


# # 3图像上绘制和写字

img = cv2.imread("2.png", cv2.IMREAD_COLOR) 
# 画一条直线
cv2.line(img, (0,0), (150,150),(255,255,255),15)

# 画一个矩形(图片， 起点，终点， 颜色（brg），宽度)
cv2.rectangle(img, (15,25), (150,200), (255,0,0), 5)

# 画一个圆形(图片， 起点，半径， 颜色（brg），宽度(-1实心))
cv2.circle(img, (105,25), 30, (0,255,0), 5)
# 画点点
pts = np.aray([[10,20],[50,60],[80,90],[100,20],[50,0]])
# pts = pts.reshape((-1, 1 ,2))
cv2.polylines(img, [pts], True, (0,255,255),5)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV Tuts!',(0,130), font, 1, (200,255,155), 2, cv2.LINE_AA)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()