# -*- coding: cp936 -*-
import json

import requests

def sms_post(data):
    headers = {
        'content-type': 'application/json',
        'access_token': '123'
    }
    url = 'http://10.47.187.165:8090/sms'
    data = {'mobiles': ['15819851862'], 'content': u'死肥籽'}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r

if __name__ == '__main__':
    r = sms_post('123')
    print r.headers
    print r.status_code
    print r.text
