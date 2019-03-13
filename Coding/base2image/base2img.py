import base64
import json
import cv2
import numpy as np


ss = "" 
with open(r"F:\PYcode\Coding\base2image\testV2.txt", "r") as f:
    ss = f.read()
print("*"*100)
print(ss)

img = base64.b64decode(ss) 

file = open(r'F:\PYcode\Coding\base2image\test2.jpg','wb') 
file.write(img)  
file.close()
