import time
import selenium
from selenium import webdriver
    

def main(url):
    driver = webdriver.Chrome(executable_path = 'F:/PYcode/Coding/crawler/chromedriver.exe')    
    driver.get(url)
    time.sleep(12)


if __name__ == "__main__":
    url = 'http://www.baidu.com'
    main(url)