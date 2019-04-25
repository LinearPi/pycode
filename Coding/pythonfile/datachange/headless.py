from selenium import webdriver
import time
# 创建chrome参数对象

opt = webdriver.ChromeOptions()

# 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
opt.set_headless()

# 创建chrome无界面对象
driver = webdriver.Chrome(options=opt)

# 访问网站
driver.get('http://59.225.209.96/portal')
name = 'sngtj_bdc'
password = 'asdfghjkl123*'
driver.find_element_by_xpath('//*[@id="username"]').send_keys(name)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[4]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="popup_one"]/div/div[2]/span[2]').click()
time.sleep(1)
# 获取cooks
cook1 = []

cookies = driver.get_cookies()
for cookie in cookies:
    cook1.append(cookie['name']+'='+ cookie['value'])
cook_str = ';'.join(cook1)
print(cook_str)

#打印内容