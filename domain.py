# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     domain 
   Description :   None
   Author :        LSQ
   date：          2020/7/17
-------------------------------------------------
   Change Activity:
                   2020/7/17: None
-------------------------------------------------
"""

from settings import MAX_SCORE

class Proxy(object):
    def __init__(self, ip=None, port=None, protocol_type=-1, anonymous_type=-1, idle=-1, area=None, score=MAX_SCORE, disable_domains=[]):
        # 代理IP的ip地址
        self.ip = ip
        # 端口号
        self.port = port
        # 协议类型，0：http，1：https，2：http&https，默认为-1
        self.protocol_type = protocol_type
        # 匿名程度，0：透明，1：匿名，2：高匿，默认为-1
        self.anonymous_type = anonymous_type
        # 响应时间
        self.idle = idle
        # 所属地区
        self.area = area
        # 评分
        self.score = score
        # 不可用域名列表
        self.disable_domains = disable_domains

    def __str__(self):
        return str(self.__dict__)