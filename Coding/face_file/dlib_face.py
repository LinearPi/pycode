#coding=utf-8
 
import cv2
import dlib
import numpy as np
 
path = r"F:\PYcode\faceinfo\007.jpg"
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
#人脸分类器
detector = dlib.get_frontal_face_detector()
# 获取人脸检测器
predictor = dlib.shape_predictor(
    r"F:\PYcode\faceinfo\dlib_shapedata\shape_predictor_68_face_landmarks.dat"
)
 
dets = detector(gray, 1)
for face in dets:
    shape = predictor(img, face)  # 寻找人脸的68个标定点
    # 遍历所有点，打印出其坐标，并圈出来
    face_list = []
    for pt in shape.parts():
        pt_pos = (pt.x, pt.y)
        face_list.append(pt_pos)
        cv2.circle(img, pt_pos, 2, (0, 255, 0), 1)
    print(face_list[0])
    print(face_list[1])
    
    cv2.polylines(img, [np.array(face_list[0:17])], False, (0,255,255), 1)
    cv2.polylines(img, [np.array(face_list[17:22])], False, (0,0,255), 2)
    cv2.polylines(img, [np.array(face_list[22:27])], False, (0,0,255), 2)

    cv2.polylines(img, [np.array(face_list[36:42])], True, (0,255,255), 1)
    cv2.polylines(img, [np.array(face_list[42:48])], True, (0,255,255), 1)
    # cv2.polylines(img, [np.array(face_list[0:16])], (0,0,255),1)
    cv2.imshow("image", img)
 
cv2.waitKey(0)
cv2.destroyAllWindows()
 