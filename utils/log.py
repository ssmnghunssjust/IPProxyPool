# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log 
   Description :   None
   Author :        LSQ
   date：          2020/7/17
-------------------------------------------------
   Change Activity:
                   2020/7/17: None
-------------------------------------------------
"""

import sys
import logging

from settings import LOG_LEVEL, LOG_FILENAME, LOG_DATEFMT, LOG_FMT


class Logger(object):
    def __init__(self):
        # 获取logger对象
        self._logger = logging.getLogger()
        # 设置formart对象
        self.formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATEFMT)
        # 设置日志输出
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        self._logger.addHandler(self._get_console_handler())
        # 设置日志等级
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self, filename):
        '''
        获取文件日志handler
        :param filename: 文件名
        :return: filehandler
        '''
        # 实例化filehandler类
        filehandler = logging.FileHandler(filename=filename, encoding='utf-8')
        # 设置日志格式
        filehandler.setFormatter(self.formatter)
        return filehandler

    def _get_console_handler(self):
        '''
        获取终端日志handler
        :return: consolehandler
        '''
        # 实例化streamhandler类
        consolehandler = logging.StreamHandler(sys.stdout)
        # 设置日志格式
        consolehandler.setFormatter(self.formatter)
        return consolehandler

    @property
    def logger(self):
        return self._logger


# 初始化Logger，通过property获得一个单例logger对象
logger = Logger().logger

if __name__ == '__main__':
    logger.debug('调试信息')
    logger.info('状态信息')
    logger.warning('警告信息')
    logger.error('错误信息')
    logger.critical('严重错误信息')
