import requests
import re
import xml
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


url_login = 'http://59.225.209.96/portal'
name = 'sngtj_bdc'
password = 'asdfghjkl123*'


def get_data(url_login, name, password):
    
    # chrome_options = Options()    
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless')
    # chrome_options.binary_location= r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    # driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="chromedriver.exe")
    # # 设置无界面
    # opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # driver = webdriver.Chrome(options=opt, executable_path="chromedriver.exe")

    
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url_login)
    driver.maximize_window()

    driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[4]').click()
    time.sleep(5)
    cook = []
    cookies = driver.get_cookies()
    print(f'cookies:{cookies}')
    for cookie in cookies:
        cook.append(cookie['name']+'='+ cookie['value'])
    cook_str = '; '.join(cook)
    print(f"cook_str:{cook_str}")
    return cook_str

def hand_cook():
    cook = ['SESSION=52b94a31-9eec-4605-8742-e05617613897', 'route=1c6037d6c177698822f08dddc01d18c6', 
            'route=977673cdcfb610a693fa9d7361b17f31', 'SESSION=b185554f-27af-4e8b-a54c-edfa84514c34']
    cook_str = '; '.join(cook)
    print(cook_str)


def get_usl_resourse(url, name, password):
    cook = get_data(url_login, name, password)

    Haeders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cook,
        "Host": "59.225.209.96",
        "Referer": "http://59.225.209.96/affair/edit/0?busiType=1&applyType=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    response = requests.get(url, headers=Haeders)
    print(response.status_code)
    # print(response.text)


if __name__ == "__main__":
    timess = int(time.time() * 1000)
    url = 'http://59.225.209.96/affair/edit/0?busiType=1&applyType=0'
    # url = 'http://59.225.209.96/portal'
    name = 'sngtj_bdc'
    password = 'asdfghjkl123*'
    # get_data(url_login, name, password)
    get_usl_resourse(url, name, password)
    # hand_cook()
    