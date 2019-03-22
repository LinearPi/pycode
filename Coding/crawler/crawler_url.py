import time
import selenium
from selenium import webdriver
from PIL import Image, ImageEnhance
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

def get_info(url, name, pad, mission):
    # 点击登录
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/ul/li[4]').click()
    # 获取图片并识别
    driver = webdriver.Chrome(executable_path = 'F:/PYcode/Coding/crawler/chromedriver.exe')    
  
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)
    driver.save_screenshot(r'F:\PYcode\Coding\crawler\all.png')
    # # 获取图片的xy轴
    # # 定位验证码
    imgelement = driver.find_element_by_xpath('//*[@id="yz"]')
    # # 写成我们需要截取的位置坐标
    # rangle = ()
    # if imgelement.location:
    #     location = imgelement.location  #获取验证码x,y轴坐标
    #     size=imgelement.size  #获取验证码的长宽
    #     rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),
    #             int(location['y']+size['height'])) #写成我们需要截取的位置坐标
    # else:
    rangle = (1010,275,1110,308)
    i = Image.open(r"F:\PYcode\Coding\crawler\all.png")  # 打开截图

    frame4 = i.crop(rangle)  
    # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save(r'F:\PYcode\Coding\crawler\resout.png')  
    imageCode = Image.open(r'F:\PYcode\Coding\crawler\resout.png')
    # 获取验证码图片，读取验证码
    text = pytesseract.image_to_string(imageCode) 
    code = ''.join(text.split())
    # 收到验证码，进行输入验证
    print(text, '*',code)
    # 输入帐号
    driver.find_element_by_xpath('//*[@id="loginName"]').send_keys(name)
    # 输入密码
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(pad)
    # 输入验证码
    driver.find_element_by_xpath('//*[@id="yzm"]').send_keys(code)
    # 输入之后登录
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[6]/a').click()
    time.sleep(3)
    cookie = ''
    ss = driver.get_cookies()
    print(ss)
    
    for idd in ss:
        cookie = idd["name"] + "=" + idd["value"]
    print(cookie) 
    # cookiestr = ';'.join(item for item in cookie)  
    # with open("TXTT.txt", "w") as f:
    #     f.write(cookiestr)
    
    uurl = driver.current_url
    pattern = re.compile('[A-Za-z0-9]{32}')
    sid_unm = pattern.search(uurl)[0]
    # 跳转到新的页面
    sid_url = f'http://192.168.1.55:85/task/addTaskPage?sid={sid_unm}&version=undefined'

    print(sid_url)
    js=f'window.open("{sid_url}");' #通过执行js，开启一个新的窗口
    print("123")
    driver.execute_script(js)
    print("456")
    allhandles = driver.window_handles
    print(allhandles)
    driver.switch_to_window(allhandles[1])

    

    # 点击任务
    # driver.find_element_by_xpath('//*[@id="headDiv"]/div/div/div[2]/div/ul/li[2]/a').click()
    # time.sleep(1)
    # # 点击普通任务
    # driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div[2]/button[3]').click()
    # # 点击项目任务
    # driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div[2]/button[1]').click()
    # driver.find_element_by_xpath('//*[@id="taskName"]').send_keys("dsgauifgash")
  
    driver.find_element_by_xpath('//*[@id="taskName"]').send_keys(mission['title'])

    print("tianxiechenggong")
    # driver.find_element_by_xpath('//*[@id="contentBody"]/div/div[2]/div/div/div/ul[2]/li/div[2]/a/i').click()
    # time.sleep(1)
    # driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[1]/div/img').click()
    # driver.find_element_by_xpath('//*[@id="layui-layer2"]/div[2]/a[1]').click()
    
    driver.switch_to.frame('eWebEditor1')
    driver.find_element_by_xpath('/html/body').send_keys(mission['des'])
    # 写好数据之后保存
    driver.switch_to_default_content()
    driver.find_element_by_xpath('//*[@id="addTask"]').click()
   
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    name = "admin"
    pad = "111111"
    url = "http://192.168.1.55:85/login.jsp"
    mission= {"title": "今天做了一个测试",
              "des": "使用selenium做了一个自动登录的尝试"}
    get_info(url,name, pad, mission)
