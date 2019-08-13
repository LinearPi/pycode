# -- coding:utf-8 --
import cv2
import sys
#由于我的图片路径包含中文，所以先转码
reload(sys)
sys.setdefaultencoding('utf-8')
im_path='hand.jpg'
save_path='hand_mask.jpg'
im=cv2.imread(im_path.encode('gbk'),1)
en=False#使能，鼠标左键开启
#鼠标事件
def draw(event,x,y,flags,param):
   global en
   if event==cv2.EVENT_LBUTTONDOWN:
      en=True#使能开启
   elif event==cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_LBUTTONDOWN:
      if en:        
          drawMask(y,x)#强行打码
      elif event==cv2.EVENT_LBUTTONUP:
          en=False
#打码函数         
def drawMask(x,y,size=10):
    #为了让码好看一些,做了一个size*size的分区处理
    X=x/size*size  
    Y=y/size*size
    print(X,Y)
    for i in range(size):
        for j in range(size):
            im[X+i][Y+j]=im[X][Y]
cv2.namedWindow('image') 
cv2.setMouseCallback('image',draw)
while(1): 
    cv2.imshow('image',im) 
    if cv2.waitKey(10)&0xFF==27: #‘esc’退出
        break
    elif cv2.waitKey(10)&0xFF==115:#‘s’键保存图片
        cv2.imwrite(save_path.encode('gbk'),im)
cv2.destroyAllWindows()
