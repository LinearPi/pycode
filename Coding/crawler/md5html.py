

import urllib
import json
import sys
from html.parser import HTMLParser
from html.entities import entitydefs
reload(sys) 
sys.setdefaultencoding('utf-8')
 
class titlehtml(HTMLParser):
    def __init__(self):
        self.title=[]
        self.readingtitle=''
        self.myfilter=''
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag==self.myfilter:
            self.readingtitle=1
    def handle_data(self, data):
        if self.readingtitle:
            self.title.append(data)
    def handle_endtag(self, tag):
        if tag==self.myfilter:
            self.readingtitle=0
 
    def gettile(self):
        return self.title
 
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inputvalue = {}
 
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "input":
            if len(attrs) == 0: pass
            else:
                for (variable, value)  in attrs:
 
                    if variable=="name":
                        self.inputvalue.setdefault(value,'')
                        myname=value
                    if variable == "value":
                        self.inputvalue[myname]=value
 
def httpget(geturl,getdata,Referer):
    urldata=urllib.quote(getdata)
    url=geturl+urldata
    headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1","Referer":Referer}
    req = urllib2.Request(url,headers=headers)
    resul=urllib2.urlopen(req).read()
    return resul
 
def httppost(geturl,getdata,Refererdata):
    data=getdata
    url=geturl
    post_data=urllib.urlencode(data)
    headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1","Referer":Refererdata}
    req=urllib2.Request(url,headers=headers,data=post_data)
    resul=urllib2.urlopen(req).read()
    return resul
 
def somd5(md5):
    url="http://www.somd5.com/somd5-index-md5.html"
    data={}
    data["isajax"]="2d6GbG7ktvGRzxJacdeI7pt"
    data["md5"]=md5
    str=httppost(url,data,"")
    newsparser = titlehtml()
    newsparser.myfilter='h1'
    newsparser.feed(str)
    items = newsparser.gettile()
    if len(items)==0:
        print("somd5没有查到")
    else:
        print("somd5查到的："+items[0])
 
def cmd5(md5):
    data=""
    res=httpget("http://www.cmd5.com/",data,"")
    viewstaut=MyHTMLParser()
    viewstaut.feed(res)
    post_data=viewstaut.inputvalue
    post_data["ctl00$ContentPlaceHolder1$TextBoxInput"]=md5
    post_data["__EVENTTARGET"]=""
    post_data["ctl00$ContentPlaceHolder1$InputHashType"]="md5"
    post_data["ctl00$ContentPlaceHolder1$HiddenField1"]="0"
    finres=httppost("http://www.cmd5.com/",post_data,"http://www.cmd5.com/")
    newsparser = titlehtml()
    newsparser.myfilter='span'
    newsparser.feed(finres)
    items = newsparser.gettile()
    if len(items)==0:
        print("cmd5没有查到")
    else:
        print("cmd5查到的："+items[3])
 
 
def hkc5(md5):
    url="http://md5.hkc5.com//index.asp?action=look"
    data={}
    data["look"]="查询"
    data["md5text"]=md5
    str=httppost(url,data,"http://md5.hkc5.com/index.asp")
    finres=MyHTMLParser()
    finres.feed(str)
    mingwen=finres.inputvalue
    try:
        print("hkc5查到的:"+mingwen["rr2"])
    except:
        print("hkc5没有查到")
 
def xx95(md5):
    data=""
    res=httpget("http://md5.xx95.net/default.html",data,"")
    viewstaut=MyHTMLParser()
    viewstaut.feed(res)
    post_data=viewstaut.inputvalue
    for key,value in post_data.items():
        if post_data[key]=="\xe8\xaf\xb7\xe8\xbe\x93\xe5\x85\xa5MD5\xe6\x88\x96\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe7\x9a\x84\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2":
            post_data[key]=md5
    finres=httppost("http://md5.tellyou.top/default.html",post_data,"http://md5.tellyou.top/default.html")
    newsparser = titlehtml()
    newsparser.myfilter='span'
    newsparser.feed(finres)
    items = newsparser.gettile()
    try:
        print("md5.tellyou的md5查询结果："+items[0])
    except:
        print("md5.tellyou的md5查询结果：没找到,请尝试其他同类网站")
 
def syue(md5):
    finstr=httpget("http://md5.syue.com/ShowMD5Info.asp?GetType=ShowInfo&md5_str=",md5,"http://md5.syue.com/")
    newsparser = titlehtml()
    newsparser.myfilter='span'
    newsparser.feed(finstr)
    items = newsparser.gettile()
    try:
        print("md5.syue的md5查询结果(乱码证明没有查到)："+items[0])
    except:
        print("md5.syue没有查到")
 
def pmd5(md5):
    data=""
    res=httpget("http://pmd5.com/",data,"")
    viewstaut=MyHTMLParser()
    viewstaut.feed(res)
    post_data=viewstaut.inputvalue
    post_data["key"]=md5
    finres=httppost("http://pmd5.com/",post_data,"http://pmd5.com/")
    newsparser = titlehtml()
    newsparser.myfilter='em'
    newsparser.feed(finres)
    items = newsparser.gettile()
    try:
        print("pmd5的md5查找结果："+items[1])
    except:
        print("pmd5没有找到")
 
def wmd5(md5):
    url="http://www.wmd5.com/ajax.php"
    data={}
    data["miwen"]=md5
    data["action"]="md5show"
    finstr=httppost(url,data,"http://www.wmd5.com/")
    d1=json.JSONDecoder().decode(finstr)
    try:
        print("wmd5查询的结果是："+d1['md5text'])
    except:
        print("wmd5没有查到")
 
def heimd5(md5):
    url="http://121.42.198.24//php/md5.php"
    data={}
    data["key"]=md5
    finstr=httppost(url,data,"http://121.42.198.24/php/md5.php")
    print("121.42.198.24的结果是："+finstr)
#def xmd5(md5):
 
 
 
 
if __name__=='__main__':
    # md5=sys.argv[1]
    # print md5
    md5="d8b521d9c8591a897704b83d18ec988d"
    somd5(md5)
    # hkc5(md5)
    # xx95(md5)
    # syue(md5)
    # pmd5(md5)
    # wmd5(md5)
    # heimd5(md5)
    # cmd5(md5)

