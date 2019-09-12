
import requests
from lxml import etree

url = "https://www.lz13.cn/mingrenmingyan/17341.html"
r = requests.get(url)
r.encoding="utf-8"
html = r.text
# print(html)
selector = etree.HTML(html)
quotes = []

for i in range(2,102):
    one = selector.xpath('//*[@id="node-8890"]/div[2]/p[' + str(i) + ']')
    quotes.append(one[0].text)
    print(one[0].text)


import random
print(random.choice(quotes))