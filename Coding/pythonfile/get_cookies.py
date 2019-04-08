import sys
import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
chrome_options = Options()

def get_data(url, name, password):
    t1 = time.time()
    chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    driver=webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    # 输入账号和密码登陆
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="btn_close"]').click()
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[4]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="popup_one"]/div/div[2]/span[2]').click()
    # 获取cooks
    cook1 = []
    cookies = driver.get_cookies()
    for cookie in cookies:
        cook1.append(cookie['name']+'='+ cookie['value'])
    cook_str = ';'.join(cook1)
    t2 = time.time()
    print(t2 - t1)
    print(cook_str)
    return cook_str

def get_usl_resourse(cook):
    url = 'http://59.225.209.96/affair/edit/0?busiType=1&applyType=0'
    t3 = time.time()
    Haeders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cook,
        "Host": "59.225.209.96",
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    response = requests.get(url, headers=Haeders)
    print(response.status_code)
    print(response.text)
    t4 = time.time()
    print(t4 - t3)


if __name__ == "__main__":
    url = r"http://59.225.209.96/portal"
    name = 'sngtj_bdc'
    # name = sys.argv[1]
    password = 'asdfghjkl123*'
    # password = sys.argv[2]
    cook = get_data(url, name, password)
    get_usl_resourse(cook)
