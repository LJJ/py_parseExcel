# coding=utf-8
import urllib
import urllib2
import json
import hashlib

kPublicKey = "TczAFlw@SyhYEyh*"

def md5(raw_str):
    m = hashlib.md5()
    m.update(raw_str)
    return m.hexdigest()

def verify():

    test_data = {'version':'1.4','user_name':'你好哈ljj妹的','user_id':'l232jljjlklj','sys':'9.0'}
    all_value = ''
    for key in sorted(test_data.keys()):
        all_value += test_data[key]
    all_value += kPublicKey
    token = md5(all_value)

    test_data['token']=token
    test_data_urlencode = urllib.urlencode(test_data)

    requrl = "http://api.lujiji.com/tbcweak/user/register"
    # requrl = "http://127.0.0.1:8000/user/register"

    req = urllib2.Request(url=requrl,data=test_data_urlencode)

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    amount = json.loads(res)
    # print amount
    return amount["result"]["message"] == "ok"