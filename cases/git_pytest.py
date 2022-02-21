import json

import requests
import pytest


def test_apiss():
    url = 'http://api.kankanyz.com/company-service/v1.1.1/jobInfo/planet/'

    """通过params传参"""
    res = requests.get(url, verify=False)

    print(res.text)
    print('请求url: ' + res.url)
    print('响应内容 json格式: ' + json.dumps(res.json()))
    print('响应内容 字符串格式: ' + res.text)
    print('响应内容 二进制格式: ' + str(res.content))
    print('响应码: ' + str(res.status_code))


def test_apiss2():
    url = 'https://tapi.kankanyz.com/jobhunter-service/userpassport/sms/login'
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    data = {
        "mobile": "18276424347",
        "code": "220119",
        "jsCode": "013DASkl2Khzu84odnol2ayvSi4DASki",
        "source": "0",
        "userType": "2"
    }

    """通过params传参"""
    # res2 = requests.post(url,headers=headers, data=json.dumps(data))
    kwargs = {'headers': {'Content-Type': 'application/json;charset=UTF-8'}, 'params': None,
              'data': None, 'json': {'mobile': '18276424347', 'code': '220119', 'source': '0', 'userType': '2'}}
    res2 = requests.request('post', url, **kwargs)
    print(res2.text)
    print('请求url: ' + res2.url)


if __name__ == '__main__':
    pytest.main(['-s', '-x', 'git_pytest.py'])
