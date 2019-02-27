import requests
from lxml import etree
import csv
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


suggestion_list= []

def selenium_get_info(url, file_name):
    # 设置无界面
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 打开浏览器，指明浏览器
    driver = webdriver.Chrome('/Users/gouweiqi/Documents/code_py/code_file/nlp4govern/chromedriver', chrome_options=chrome_options) 
    # 输入网址
    driver.get(url)
    # 等待网页加载
    driver.set_window_size(1400,900)
    driver.implicitly_wait(5)
    time.sleep(5)

    # 获取到有多少页面的数据
    pagename = driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/div/table/tbody/tr/td[5]').text
    pattarn = re.compile(r'\d+')
    all_page = pattarn.findall(pagename)
    all_name = int(all_page[0])

    # 存入数据，以字典的形式传入
    with open(file_name, 'w') as csvfile:
        fieldnames = ['url_address', 'title', 'content', 'serial_number', 'push_time', 'status', 'ans_content', 'ans_part', 'ans_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for xx in range(all_name):
            # 每页有十条数据：
            for i in range(1,11):
                # 保存数据的网络地址                      
                url_click = driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/table[' + str(i) + ']/tbody/tr/td[3]/a').get_attribute("href")
                # 点击进入详细网页
                driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/table[' + str(i) + ']/tbody/tr/td[3]/a').click()
                # 切换浏览器的窗口
                winders = driver.window_handles
                driver.switch_to_window(winders[1])
                # 等待1秒钟加载页面
                time.sleep(1)
                # 获取需要的信息
                title = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[2]/tbody/tr[1]/td[2]').text
                content = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]').text
                serial_number = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[2]/tbody/tr[3]/td[2]').text
                push_time = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[2]/tbody/tr[4]/td[2]').text
                status = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[4]/tbody/tr[1]/td[2]').text
                ans_content = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[4]/tbody/tr[2]/td[2]').text
                ans_part = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[4]/tbody/tr[3]/td[2]').text
                ans_time = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[4]/div/table/tbody/tr/td/table[4]/tbody/tr[3]/td[4]').text
                #
                # 保存信息
                writer.writerow({'url_address':url_click, 
                                'title': title, 
                                'content':content, 
                                'serial_number':serial_number,
                                'push_time':push_time,
                                'status':status,
                                'ans_content':ans_content,
                                'ans_part':ans_part,
                                'ans_time':ans_time})
                # 关闭当前页面
                driver.close()
                # 切换到原来的页面
                driver.switch_to_window(winders[0])
            # 点击下一页
            driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/div/table/tbody/tr/td[6]').click()
            time.sleep(3)



#     i = 1
    #     while i < 14:
    #         time.sleep(5)
    #         try:
                
    #             url_click = driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/table[' + str(i) + ']/tbody/tr/td[3]/a').get_attribute("href")
    #             suggestion_list.append([url_click.get_attribute("href"), url_click.get_attribute("text")])
    #             push_time = driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/table[' + str(i) + ']/tbody/tr/td[4]').text
    #             writer.writerow({'url_address': url_click.get_attribute("href"), 'title':url_click.get_attribute("text"), 'push_time':push_time})
    #             driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/div/table/tbody/tr/td[6]').click()
    #             i += 1
    #         except:
    #             pass
    #         finally:
    #             driver.quit()
            
    #     print(suggestion_list)
    # return suggestion_list
#
# driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/table[1]/tbody/tr/td[3]/a').click()
# winders = driver.window_handles
# driver.switch_to_window(winders[1])
# messages = driver.find_elements_by_xpath('//*[@id="barrierfree_containe]/div[4]/div/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]')[0].text()
# messages[0].text
# driver.close()
# driver.switch_to_window(widn[0])
# 
# driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/table[2]/tbody/tr/td[3]/a').click()
#
# def save_message():
#     with open('names.csv', 'w') as csvfile:
#     ...:     fieldnames = ['first_name', 'last_name']
#     ...:     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     ...:
#     ...:     writer.writeheader()
#     ...:     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#     ...:     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#     ...:     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})


def get_page(url,page_num):
    pageList =[]
    for i in range(1,page_num +1):
        formdata ={"webid": 1,
            "areacode": 620000000000,
            "sysid": 2,
            "type": 2,
            "pageno": i}
        try:
            r = requests.get(url, data=formdata)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print('链接成功')
            print(r.text)
            # p = re.compile(r'href="(http://www.jdlingyu.net/\d{5}/)"')
    #         tempList = re.findall(p,r.text)
    #         for each in tempList:
    #             pageList.append(each)
    #             print('保存页面成功')
    #         tempList = []
    #     "//*[@id="pagetest2"]/div/div/table[1]/tbody/tr/td[3]/a"
        except:
            print('链接失败')
    # print(pageList)
    return "pageList"


def get_infomation(url):
    response = requests.get(url).text()
    page_one = etree.HTML(response)



def main(*message):
    with open('t_message.csv', 'w') as csvfile:
        fieldnames = ['url_address', 'title', 'push_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    writer.writerow(*message)

def test_re():
    # 打开浏览器，指明浏览器
    driver = webdriver.Chrome('/Users/gouweiqi/Documents/code_py/code_file/nlp4govern/chromedriver') 
    # 输入网址
    driver.get('http://www.gszwfw.gov.cn/gszw/zxts/frontshow.do?webid=1&sysid=2&type=2&code=001001050')
    time.sleep(3)
    # 获取页面数据总数
    pagename = driver.find_element_by_xpath('//*[@id="pagetest2"]/div/div/div/table/tbody/tr/td[5]').text
    pattarn = re.compile(r'\d+')
    all_page = pattarn.findall(pagename)
    print(int(all_page))


if __name__ == "__main__":
    url= "http://www.gszwfw.gov.cn/gszw/zxts/frontshow.do?webid=1&sysid=2&type=2&code=001001050"
    url_a = 'http://www.gszwfw.gov.cn/gszw/zxts/frontshow.do?webid=1&sysid=3&type=2&code='
    complain_url = 'http://www.gszwfw.gov.cn/gszw/zxts/frontshow.do?webid=1&sysid=4&type=2&code=001001050'
    
    file_name = './suggest_message.csv'
    file_name_a = './ask_message.csv'
    file_name_c = './complain_message.csv'

    selenium_get_info(complain_url, file_name_c)