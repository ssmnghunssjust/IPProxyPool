# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main 
   Description :   开启3个进程，分别启动爬虫，检测代理IP，web服务
        1、 定义run方法用于启动代理池
            1、 创建启动爬虫的进程，添加到列表中
            2、 创建启动检测的进程，添加到列表中
            3、 创建启动提供API服务的进程，添加到列表中
            4、 遍历进程列表，启动所有进程
            5、 遍历进程列表，让主进程等待子进程的完成
   Author :        LSQ
   date：          2020/7/22
-------------------------------------------------
   Change Activity:
                   2020/7/22: None
-------------------------------------------------
"""
from multiprocessing import Process
from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyApi

def run():
    process_list = []
    process_list.append(Process(target=RunSpider.start))
    process_list.append(Process(target=ProxyTester.start))
    process_list.append(Process(target=ProxyApi.start))

    for process in process_list:
        process.daemon = True
        process.start()

    for process in process_list:
        process.join()

if __name__ == '__main__':
    run()