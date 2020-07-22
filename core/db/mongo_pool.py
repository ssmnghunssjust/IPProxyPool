# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mongo_pool 
   Description :   对proxies集合进行数据库的相关操作
        1、 在init中建立数据库连接，获取要操作的集合，在del方法中关闭数据库连接
        2、 提供基础的增删改查功能
            1、 实现插入
            2、 修改
            3、 删除：根据ip地址进行删除
            4、 查询所有代理IP的功能
        3、 提供代理API模块使用的功能
            1、 查询功能：根据条件进行查询（指定查询数量，先分数降序，后响应速度升序进行排序）
            2、 根据协议类型和访问的目标网站域名，获取代理IP列表
            3、 根据协议类型和访问的目标网站域名，随机获取一个代理IP
            4、 把指定域名添加到指定IP的disable_domains列表中
   Author :        LSQ
   date：          2020/7/19
-------------------------------------------------
   Change Activity:
                   2020/7/19: None
-------------------------------------------------
"""
import random

import pymongo
from settings import MONGO_URI
from utils.log import logger
from domain import Proxy


class MongoPool(object):
    def __init__(self):
        # 建立数据库连接，获取集合
        self.client = pymongo.MongoClient(MONGO_URI)
        self.collection = self.client['proxy_pool']['proxy']

    def __del__(self):
        # 关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        count = self.collection.count_documents({'_id': proxy.ip})
        if count == 0:
            proxy_dict = proxy.__dict__
            proxy_dict['_id'] = proxy.ip
            self.collection.insert_one(proxy_dict)
            logger.info('插入新代理：{}'.format(proxy))
        else:
            logger.warning('已存在代理：{}'.format(proxy))

    def update_one(self, proxy):
        self.collection.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})
        logger.info('更新代理IP为：{}'.format(proxy))

    def delete_one(self, proxy):
        self.collection.delete_one({'_id': proxy.ip})
        logger.info('删除代理IP：{}'.format(proxy))

    def find_all(self):
        cursor = self.collection.find()
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        '''
        根据指定条件进行查询
        :param conditions: 查询条件字典
        :param count: 查询数量
        :return: 代理IP列表
        '''
        cursor = self.collection.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING),
            ('idle', pymongo.ASCENDING)
        ])
        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol_type=None, domain=None, count=0, anonymous_type=2):
        '''
        根据协议类型和访问的目标域名为条件进行查询
        :param protocol_type: 默认为支持http和https
        :param domain:
        :param count: 默认为0，即查询所有
        :param anonymous_type: 默认获取高匿代理IP
        :return: 满足条件的代理IP列表
        '''
        conditions = {
            'anonymous_type': anonymous_type
        }
        if protocol_type == None:
            conditions['protocol_type'] = 2
        elif protocol_type.lower() == 'http':
            conditions['protocol_type'] = {'$in': [0, 2]}
        elif protocol_type.lower() == 'https':
            conditions['protocol_type'] = {'$in': [1, 2]}
        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}
        return self.find(conditions, count)

    def random_proxy(self, protocol_type=None, domain=None, count=0, anonymous_type=2):
        proxy_list = self.get_proxies(protocol_type=protocol_type, domain=domain, anonymous_type=anonymous_type,
                                      count=count)
        proxy = random.choice(proxy_list)
        return proxy

    def disabled_domain(self, ip, domain):
        '''
        把指定域名添加到指定IP的disable_domains列表中
        :param ip:
        :param domain:
        :return:
        '''
        count = self.collection.count_documents({'_id': ip, 'disable_domains': domain})
        if count == 0:
            self.collection.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False

    def get_proxies_test(self, conditions={},count=0):
        '''
        根据协议类型和访问的目标域名为条件进行查询
        :param protocol_type: 默认为支持http和https
        :param domain:
        :param count: 默认为0，即查询所有
        :param anonymous_type: 默认获取高匿代理IP
        :return: 满足条件的代理IP列表
        '''

        return self.find(conditions, count)


if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy('122.226.57.70', 8888)
    # proxy = Proxy('122.226.57.70',9999)
    # mongo.insert_one(proxy)
    # mongo.update_one(proxy)
    # mongo.delete_one(proxy)
    # for proxy in mongo.find_all():
    #     print(proxy)
    # proxy = Proxy('122.226.57.77', 8899, protocol_type=2, anonymous_type=2, idle=5, area='china', score=20, disable_domains=['jd.com'])
    # proxy = Proxy('122.226.57.73', 8889, protocol_type=1,anonymous_type=1,idle=5,area='china',score=30, disable_domains=['jd.com'])
    # proxy = Proxy('122.226.57.74', 8890, protocol_type=0,anonymous_type=2,idle=8,area='china',score=40, disable_domains=['jd.com'])
    # mongo.insert_one(proxy)
    # mongo.update_one(proxy)
    for each in mongo.get_proxies(protocol_type='http', domain='taobao.com'):
        print(each)
    # print(mongo.random_proxy())
    print(mongo.disabled_domain('122.226.57.70', 'taobao.com'))

