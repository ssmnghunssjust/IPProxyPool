# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxy_api 
   Description :   为爬虫提供高可用的代理IP接口
        1、 根据协议类型和域名，提供随机的代理IP
        2、 根据协议类型和域名，提供多个代理IP
        3、 给指定代理IP添加禁止域名disabled_domains

        1、 创建ProxyApi类
        2、 实现init方法
            1、 初始化flask的web服务
            2、 根据协议类型和域名，提供随机代理IP
                1、 通过protocol和domain参数对IP进行过滤
            3、 根据协议类型和域名提供多个代理IP
                1、 通过protocol和domain参数对IP进行过滤
            4、 给指定IP追加禁止域名
        3、 实现run方法，用于启动flask web服务
        4、 实现start方法，用于通过类名，启动服务
   Author :        LSQ
   date：          2020/7/22
-------------------------------------------------
   Change Activity:
                   2020/7/22: None
-------------------------------------------------
"""
import json

from flask import Flask, request
from core.db.mongo_pool import MongoPool
from settings import PROXIES_DEFAULT_COUNT
from domain import Proxy


class ProxyApi(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.mongo_pool = MongoPool()

        @self.app.route('/random/')
        def random():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol, domain, count=PROXIES_DEFAULT_COUNT)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format(proxy.ip, proxy.port)

        @self.app.route('/proxies/')
        def proxies():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol, domain, count=PROXIES_DEFAULT_COUNT)
            proxies = [{'ip': proxy.ip, 'port': proxy.port} for proxy in proxies]
            return json.dumps(proxies)

        @self.app.route('/disabled_domain/')
        def disable_domain():
            ip = request.args.get('ip', None)
            domain = request.args.get('domain', None)
            if ip is None:
                return '填写ip'
            if domain is None:
                return '填写域名'
            self.mongo_pool.disabled_domain(ip, domain)
            return '成功设置{}禁止访问{}'.format(ip, domain)

    def run(self):
        self.app.run('0.0.0.0', port=8000, debug=True)

    @classmethod
    def start(cls):
        proxy_api = cls()
        proxy_api.run()


if __name__ == '__main__':
    ProxyApi().start()
