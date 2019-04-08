import requests
import json

def getToken():

    data = json.dumps({"name":"sngtj_bdc","password":"asdfghjkl123*",})
    url = 'http://59.225.209.96/oauth2/login'
    headers = {'content-type': 'application/json'}

    resp = requests.post(
        url=url,
        data=data ,headers=headers).json()
    session_id = resp['session_id']
    #print(session_id)
    return str(session_id)
ts = getToken()
print(ts)
