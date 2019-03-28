import requests
import json

def get_test():
    url = 'https://www.eteams.cn/imrequest/queryIMInfo.json'
    Username = '807745654@qq.com'
    Password = '774875'
    Header = {"Cookie": "WEBID=93d064408ef7d0e5b9f336bddb333f74; SITEID=bc0542138ebf43b2bcba2fd8726ec925; Hm_lvt_41555f1291b274a5e1d99199f20e9eab=1553588150,1553588201,1553588228,1553588312; imWebClientId=static-3883c1bf-f263-09cd-4fae-ab602583080f; JSESSIONID=A193F316E6538116D432BEBC4FC892BC; Hm_lpvt_41555f1291b274a5e1d99199f20e9eab=1553649326; ETEAMSID=05ad064509405143debc235f3b179eab; ETEAMSID=05ad064509405143debc235f3b179eab",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
    
    r = requests.post(url, data=Header, auth=(Username, Password))
    print(r.status_code)
    print(r.text)

if __name__ == "__main__":
    get_test()

