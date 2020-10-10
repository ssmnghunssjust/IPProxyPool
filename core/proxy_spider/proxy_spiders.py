# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxy_spiders 
   Description :   None
   Author :        LSQ
   date：          2020/7/21
-------------------------------------------------
   Change Activity:
                   2020/7/21: None
-------------------------------------------------
"""
import requests
import time
import random

from lxml import etree
from domain import Proxy
from utils.http import get_random_request_headers
from core.proxy_spider.base_spider import BaseSpider


class Ip3366Spider(BaseSpider):

    urls = ['http://www.ip3366.net/?stype=1&page={}'.format(i) for i in range(1, 6)]
    group_xpath = '//div[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[6]/text()'
    }

class KuaiSpider(BaseSpider):
    urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 11)]
    group_xpath = '//div[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }
    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_random_request_headers())
        idle = random.uniform(1,3)
        # print(idle)
        time.sleep(idle)
        return response.content

class SixSixIpSpider(BaseSpider):
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 6)]
    group_xpath = '//div[@id="main"]//table/tr[position()>1]'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }

    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_random_request_headers())
        idle = random.uniform(1, 3)
        time.sleep(idle)
        # response.content.decode('GBK')
        return response.content

if __name__ == '__main__':

    # spider = Ip3366Spider()
    spider = SixSixIpSpider()
    for proxy in spider.get_proxies():
        print(proxy)

    # class A(object):
    #     value = ''
    #     def __init__(self):
    #         self.value = '2'
    #     def test(self):
    #         print(self.value)
    #
    # class B(A):
    #     value = '1'
    #
    # b = B()
    # print(b.test())