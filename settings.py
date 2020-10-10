# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     settings 
   Description :   None
   Author :        LSQ
   date：          2020/7/16
-------------------------------------------------
   Change Activity:
                   2020/7/16: None
-------------------------------------------------
"""

import logging

# Proxy类（代理IP）默认评分
MAX_SCORE = 50

# 默认的日志配置信息
LOG_LEVEL = logging.INFO
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'log.log'

# 测试代理IP的超时时间
TEST_TIMEOUT = 5

# Mongodb连接URI
MONGO_URI = 'mongodb://47.101.128.239:27017'

PROXIES_SPIDERS = [
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.KuaiSpider',
    'core.proxy_spider.proxy_spiders.SixSixIpSpider'
]

RUN_SPIDER_INTERVAL = 1

# 开启异步数量
TEST_PROXIES_ASCYNC_COUNT = 10

# 检测代理时间间隔
TEST_PROXIES_INTERVAL = 30

PROXIES_DEFAULT_COUNT = 50