# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     run_spiders
   Description :   根据配置文件信息，加载爬虫，抓取代理IP，进行校验，如果可用就写入到数据库中
        1、 在run_spiders中创建RunSpiders类
        2、 提供一个运行爬虫的run方法，作为运行爬虫的入口，实现核心的处理逻辑
            1、 根据配置文件信息获取爬虫对象列表
            2、 遍历爬虫对象列表，获取爬虫对象，遍历爬虫对象的get_proxies方法，获取代理IP
            3、 检测代理IP
            4、IP可用则入库
            5、 处理异常
        3、 使用异步执行每一个爬虫任务，提高抓取效率
            1、 在init方法中创建协程池对象
            2、 把处理一个代理爬虫的代码抽到一个方法
            3、 使用异步执行上面的方法
            4、 调用协程的join方法，让当前线程等待队列任务的完成
        4、 使用schedule模块，实现每隔一段时间，执行一次爬取任务
            1、 定义一个start的类方法
            2、 创建当前类的对象，调用run方法
            3、 使用schedule模块，每隔一段时间，执行run方法
   Author :        LSQ
   date：          2020/7/21
-------------------------------------------------
   Change Activity:
                   2020/7/21: None
-------------------------------------------------
"""

# 猴子补丁
from gevent import monkey
monkey.patch_all()
# 协程池
from gevent.pool import Pool

import importlib
import schedule
import time

from settings import PROXIES_SPIDERS
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
from settings import RUN_SPIDER_INTERVAL


class RunSpider(object):
    def __init__(self):
        self.mongo_pool = MongoPool()
        self.coroutine_pool = Pool()

    def get_spiders_from_settings(self):
        for spider in PROXIES_SPIDERS:
            module_name, spider_class = spider.rsplit('.', maxsplit=1)
            module = importlib.import_module(module_name)
            cls = getattr(module, spider_class)
            spider = cls()
            yield spider

    def run(self):
        spiders = self.get_spiders_from_settings()
        for spider in spiders:
            self.coroutine_pool.apply_async(self.__tasks, args=(spider, ))
        self.coroutine_pool.join()

    def __tasks(self, spider):
        try:
            proxies = spider.get_proxies()
            for proxy in proxies:
                # print(proxy)
                proxy = check_proxy(proxy)
                if proxy.idle != -1:
                    self.mongo_pool.insert_one(proxy)
        except Exception as e:
            logger.exception(e)

    @classmethod
    def start(cls):
        run_spider = cls()
        run_spider.run()
        schedule.every(RUN_SPIDER_INTERVAL).hours.do(run_spider.run)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    # run = RunSpider()
    # run.get_spiders_from_settings()
    # run.run()
    RunSpider().start()