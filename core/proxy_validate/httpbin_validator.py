# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     httpbin_validator 
   Description :   检查代理IP的响应速度、匿名程度、协议类型
        1、 响应速度：从发送请求到获取响应的时间间隔
        2、 匿名程度：
            1、 对http://httpbin.org/get或者https://httpbin.org/get发送请求
            2、 响应中origin中由‘，’分割的两个IP就是透明代理IP
            3、 如果响应中的headers中包含proxy-connection说明是匿名代理IP
            4、 否则就是高匿代理IP
        3、 协议类型：分别对http://httpbin.org/get和https://httpbin.org/get发送请求，成功并获取响应即支持该协议
   Author :        LSQ
   date：          2020/7/18
-------------------------------------------------
   Change Activity:
                   2020/7/18: None
-------------------------------------------------
"""
import requests
import time
import json

from utils.http import get_random_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy

def check_proxy(proxy):
    '''
    检查代理IP的响应时间、匿名程度、协议类型
    :param proxy: 代理IP对象
    :return: 代理IP对象
    '''
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
    }
    # 检测
    http, http_anonymous_type, http_idle = __check_http_proxies(proxies)
    https, https_anonymous_type, https_idle = __check_http_proxies(proxies, is_http=False)

    if http and https:
        proxy.protocol_type = 2
        proxy.anonymous_type = http_anonymous_type
        proxy.idle = http_idle if http_idle > https_idle else https_idle
    elif http:
        proxy.protocol_type = 0
        proxy.anonymous_type = http_anonymous_type
        proxy.idle = http_idle
    elif https:
        proxy.protocol_type = 1
        proxy.anonymous_type = https_anonymous_type
        proxy.idle = https_idle
    else:
        proxy.protocol_type = -1
        proxy.anonymous_type = -1
        proxy.idle = -1
    return proxy

def __check_http_proxies(proxies, is_http=True):
    anonymous_type = -1
    idle = -1
    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    try:
        # 获取开始时间
        start = time.time()
        # 发送请求，获取响应，test_url中的协议必须与proxies中的协议对应，如test_url中为http，proxies中必有http协议，否则将会使用本地ip发送请求。test_url中为https，proxies中必有https
        response = requests.get(test_url, headers=get_random_request_headers(), proxies=proxies, timeout=TEST_TIMEOUT)
        if response.ok:
            # 计算响应时间间隔
            idle = round(time.time() - start, 2)
            # 检测匿名程度
            resp = json.loads(response.text)
            # print(resp['origin'])
            if ',' in resp.get('origin'):
                anonymous_type = 0
            elif resp['headers'].get('proxy_connection', None):
                anonymous_type = 1
            else:
                anonymous_type = 2
            return True, anonymous_type, idle
        else:
            return False, anonymous_type, idle
    except Exception as e:
        # logger.exception(e)
        return False, anonymous_type, idle

if __name__ == '__main__':
    proxy = Proxy(ip='58.253.155.244',port=9999)
    print(check_proxy(proxy))

    # resp = requests.get('http://httpbin.org/get', headers=get_random_request_headers(),proxies={'http':'http://171.11.29.54:9999'})
    # resp = requests.get('https://httpbin.org/get', headers=get_random_request_headers(),proxies={'https':'https://58.253.155.244:9999'})
    # print(resp.text)
    # print(resp.status_code)
    # print(resp.ok)