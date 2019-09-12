import time
import selenium
from PIL import Image
from selenium import webdriver
import requests
from lxml import etree
import random


def main(url):
    
    driver = webdriver.Chrome(executable_path = 'F:/PYcode/Coding/crawler/chromedriver.exe')    
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)
    # 登录选择邮箱
    # driver.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()
    # # 输入账号密码登录
    # driver.find_elements_by_xpath('//*[@id="username"]')[0].send_keys(username)
    # driver.find_elements_by_xpath('//*[@id="password"]')[0].send_keys(passwd)
    # driver.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()

    # time.sleep(3)
    # # 小组
    # driver.find_element_by_xpath('//*[@id="db-global-nav"]/div/div[4]/ul/li[6]/a').click()
    # # 切换窗口
    # handles = driver.window_handles
    # driver.switch_to.window(handles[-1])
  
    # # 我的发起 
    # driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/div[2]/p/a[1]').click()
    # time.sleep(3)

    # # 第一个 
    # driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/a').click()
    # time.sleep(3)

    # # 找到输入框
    # quote = random.choice(quotes_list)
    # kw = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' UP ' + quote)
    # print(kw)

    # driver.find_element_by_xpath('//*[@id="last"]').send_keys(kw)

    # # 输入完成后点击
    # driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div[3]/form/span[1]/input')[0].click()

    # time.sleep(5)
    # driver.close()
    # driver.quit()
    
def get_word(url):
    r = requests.get(url)
    r.encoding="utf-8"
    html = r.text
    # print(html)
    selector = etree.HTML(html)
    quotes = []

    for i in range(2,102):
        one = selector.xpath('//*[@id="node-8890"]/div[2]/p[' + str(i) + ']')
        quotes.append(one[0].text)

    return quotes


if __name__ == "__main__":
    quotes_url = "https://www.lz13.cn/mingrenmingyan/17341.html"
    quotes = get_word(quotes_url)
    url = 'https://www.somd5.com/'
    username = '807745654@qq.com'
    passwd = 'li15280221'

 
    main(url)
      
