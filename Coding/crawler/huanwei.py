import time
import selenium
from PIL import Image
from selenium import webdriver

# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
def main(url, username, passwd):
    
    driver = webdriver.Chrome(executable_path = 'F:/PYcode/Coding/crawler/chromedriver.exe')    
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/ul/li[4]/a').click()
    # driver.save_screenshot('All.png') # 截取当前网页，该网页有我们需要的验证码
    # imgelement = driver.find_element_by_xpath('//*[@id="yz"]')
    # location = imgelement.location # 获取验证码x,y轴坐标
    # size = imgelement.size # 获取验证码的长宽
    # rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
    #  # 写成我们需要截取的位置坐标
    # i = Image.open("All.png") # 打开截图
    # result = i.crop(rangle) # 使用Image的crop函数，从截图中再次截取我们需要的区域
    # result.save('result.png')
    # text = pytesseract.image_to_string('result.png', 'eng').strip()
    # print(text)

    driver.find_elements_by_xpath('//*[@id="username"]')[0].send_keys(username)
    driver.find_elements_by_xpath('//*[@id="password"]')[0].send_keys(passwd)
    # driver.find_elements_by_xpath('//*[@id="yzm"]')[0].send_keys(text)
    time.sleep(1)
    driver.find_elements_by_xpath('//*[@id="loginForm"]/div[5]/button')[0].click()
    cookies = driver.get_cookies()
    cook_list = []
    for cook in cookies:
        cook_list.append(cook['name']+ '=' +cook['value'])
    print(cook_list)

    
    time.sleep(10)
    driver.close()
    driver.quit()
    


if __name__ == "__main__":
    url = 'https://passport.eteams.cn/login'
    username = 'zzqrrl@163.com'
    passwd = 'zzq19910526'
    main(url,username, passwd)
807745654@qq.com
774875
hearders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
data = {'username':"807745654@qq.com",
        'password':"774875"}