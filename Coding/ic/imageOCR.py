# coding = utf-8
import pytesseract
import cv2
import pyocr 
from PIL import Image
from PIL.ImageOps import invert
import time

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
image = Image.open('F:/PYcode/Coding/ic/address.jpg', mode='r').convert("L")
image.save(f'F:/PYcode/Coding/ic/{time.localtime().tm_hour}{time.localtime().tm_min}.png', quality=50)
text = pytesseract.image_to_string(image, lang='chi_sim')
print(text.replace(' ',''))  



# print(image.mode)


# # print(type(image))
# image = invert(image)
# image= image.convert('1')

# .convert("L")
# 转灰色
# convert("L")
# 切片
# crop (left, upper, right, lower)-tuple.
# new_image = image.crop((0,68,500,310))

# 保存灰色图片

# 保存文本信息
# with open('chi.txt','a',encoding='utf-8') as f:
    # f.write(text)





