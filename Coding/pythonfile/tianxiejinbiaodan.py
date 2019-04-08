import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data(url, name, password):
    t1 = time.time()
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    cook2 = []
    cookies = driver.get_cookies()
    for cookie in cookies:
        cook2.append(cookie['name']+'='+ cookie['value'])
    print(cook2)

    driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[4]').click()
    cook1 = []
    cookies = driver.get_cookies()
    for cookie in cookies:
        cook1.append(cookie['name']+'='+ cookie['value'])
    print(cook1)
    time.sleep(1)
    # cookies = driver.get_cookies()
    # t2 = time.time()
    # print(cookies)
    # print(t2-t1)
    driver.find_element_by_xpath('//*[@id="popup_one"]/div/div[2]/span[2]').click()
    driver.find_element_by_xpath('//*[@id="navigate-top"]/li[2]').click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="navigate-left"]/li[4]/div/span').click()
    
    # 执行js
    js = "var q=document.getElementsByClassName(\"menu-list\")[0]; q.style = \"\";"
    driver.execute_script(js)
    driver.find_element_by_xpath('//*[@id="navigate-left"]/li[4]/ul/li[4]/p').click()
    driver.find_element_by_xpath('//*[@id="navigate-left"]/li[4]/ul/li[4]/ul/li[1]/p').click()
    # 跳转到iframe
    iframe1 = driver.find_element_by_xpath('//*[@id="right_tab"]/div[2]/div[2]/div/iframe')
    driver.switch_to.frame(iframe1)
    # 点击新增

    ss = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/a').text
    print(ss)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/a/span/span[1]').click() 

    # 获取一级事项
    time.sleep(1)
    yiji_sx = driver.find_element_by_xpath('//*[@id="_easyui_tree_1"]/span[3]/span').text
    print(yiji_sx)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="_easyui_tree_1"]/span[3]/span').click()
    
    # 获取二级事项
    time.sleep(5)
    erji_sx = driver.find_element_by_xpath('//*[@id="_easyui_tree_3"]/span[4]/span').text
    print(erji_sx)
    driver.find_element_by_xpath('//*[@id="_easyui_tree_3"]/span[4]/span').click()

    # 获取三级事项
    time.sleep(5)
    sanji_sx = driver.find_element_by_xpath('//*[@id="_easyui_tree_24"]/span[6]/span').text
    print(sanji_sx)
    driver.find_element_by_xpath('//*[@id="_easyui_tree_24"]/span[6]/span').click()
    # 选择其他的表单来填写
    cook = []
    cookies = driver.get_cookies()
    for cookie in cookies:
        cook.append(cookie['name']+'='+ cookie['value'])
    print(cook)
    time.sleep(10)
    

    


if __name__ == "__main__":
    # url = r"https://59.225.209.96/auth/oauth/authorize?response_type=code&client_id=SampleClientId2&redirect_uri=http%3A%2F%2F59.225.209.96%3A80%2Fmain%2Flogin&scope=user_info&state=F2mMO"
    url = r"http://59.225.209.96/portal"

    # name = "sn_admin"
    # password = "zwzx7726@"
    name = 'sngtj_bdc'
    password = 'asdfghjkl123*'
    get_data(url, name, password)
