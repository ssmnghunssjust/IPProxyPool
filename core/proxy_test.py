# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxy_test 
   Description :   检查代理可用性，保证代理池中的IP基本可用
        1、 创建ProxyTester类
        2、 提供一个run方法，用于处理检测核心逻辑
            1、 从数据库中获取所有代理IP
            2、 遍历代理IP列表
            3、 检查代理IP可用性
                1、 如果代理IP不可用，让其分数减1，如果分数为0则从数据库中删除该IP
                2、 如果代理可用，就恢复为MAX_SCORE
        3、 使用异步执行检测任务，提高检测速度
            1、 把待检测IP放入队列中
            2、 把检查一个代理可用性的代码，抽取到一个方法中，从队列中获取代理IP，进行检查；检查完毕，调度队列的task_done方法
            3、 通过异步回调，使用死循环不断执行这个方法
            4、 开启多个一个异步任务，来处理代理IP的检测，可以通过配置文件指定异步数量
        4、 使用schedule模块，每隔一定时间执行一个检测任务
            1、 定义一个start的类方法
            2、 创建当前类的对象，调用run方法
            3、 使用schedule模块，每隔一段时间，执行run方法
   Author :        LSQ
   date：          2020/7/22
-------------------------------------------------
   Change Activity:
                   2020/7/22: None
-------------------------------------------------
"""
import schedule
import time

from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCORE, TEST_PROXIES_ASCYNC_COUNT, TEST_PROXIES_INTERVAL
from queue import Queue


class ProxyTester(object):
    def __init__(self):
        self.mongo_pool = MongoPool()
        self.q = Queue()
        self.coroutine_pool = Pool()

    def run(self):
        proxies = self.mongo_pool.find_all()
        for proxy in proxies:
            self.q.put(proxy)
        for i in range(TEST_PROXIES_ASCYNC_COUNT):
            self.coroutine_pool.apply_async(self.__task, callback=self.__check_callback)
        self.q.join()

    def __check_callback(self, tmp):
        self.coroutine_pool.apply_async(self.__task, callback=self.__check_callback)

    def __task(self):
        proxy = check_proxy(self.q.get())
        if proxy.idle == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.update_one(proxy)
        else:
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        self.q.task_done()

    @classmethod
    def start(cls):
        proxy_tester = cls()
        proxy_tester.run()

        schedule.every(TEST_PROXIES_INTERVAL).minutes.do(proxy_tester.run)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    ProxyTester().start()
