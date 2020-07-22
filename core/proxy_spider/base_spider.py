# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     base_spider 
   Description :   通用爬虫，聚焦爬虫的基类
        1、 在base_spider.py文件中定义一个BaseSpider类，集成自object
        2、 提供三个类成员变量
            1、 urls： 代理网站的url列表，也是待爬取url的列表
            2、 group_xpath： 分组xpath，获取包含代理IP信息标签列表xpath，其实就是一个ip即一个组
            3、 detail_xpath： 组内xpath，获取代理IP详情的信息xpath，格式为：{'ip':xxx,'port':xxx,'area':xxx}
        3、 提供初始方法，传入爬虫url列表，分组xpath，详情xpath
        4、 对外提供一个获取代理IP的方法
            1、 遍历url列表，获取url
            2、 根据发送请求，获取页面数据
            3、 解析页面，提取数据，封装为Proxy对象
            4、 返回Proxy对象列表
   Author :        LSQ
   date：          2020/7/20
-------------------------------------------------
   Change Activity:
                   2020/7/20: None
-------------------------------------------------
"""
import requests

from lxml import etree
from domain import Proxy
from utils.http import get_random_request_headers


class BaseSpider(object):
    urls = []
    group_xpath = ''
    detail_xpath = {
        'ip': '',
        'port': '',
        'area': ''
    }

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_random_request_headers())
        return response.content

    def get_proxies_from_page(self, page):
        html = etree.HTML(page)
        trs = html.xpath(self.group_xpath)
        for tr in trs:
            ip = tr.xpath(self.detail_xpath['ip'])[0] if len(tr.xpath(self.detail_xpath['ip'])) > 0 else None
            port = tr.xpath(self.detail_xpath['port'])[0] if len(tr.xpath(self.detail_xpath['port'])) > 0 else None
            area = tr.xpath(self.detail_xpath['area'])[0] if len(tr.xpath(self.detail_xpath['area'])) > 0 else None
            proxy = Proxy(ip=ip, port=port, area=area)
            yield proxy

    def get_proxies(self):
        for url in self.urls:
            print(url)
            page = self.get_page_from_url(url)
            proxies = self.get_proxies_from_page(page)
            yield from proxies


if __name__ == '__main__':
    # pass
    config = {
        'urls': ['http://www.ip3366.net/?stype=1&page={}'.format(i) for i in range(1, 4)],
        'group_xpath': '//div[@id="list"]/table/tbody/tr',
        'detail_xpath': {
            'ip': './td[1]/text()',
            'port': './td[2]/text()',
            'area': './td[6]/text()'
        }
    }
    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)
