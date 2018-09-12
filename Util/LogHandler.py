# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     LogHandler.py
   Description :  日志操作模块
   Author :       lf
   date：         2017/3/6
-------------------------------------------------
   Change Activity:
                   2017/3/6: log handler
                   2017/9/21: 屏幕输出/文件输出 可选(默认屏幕和文件均输出)
-------------------------------------------------
"""
__author__ = 'lf'

import os
import sys
import logging

from logging.handlers import TimedRotatingFileHandler

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

LOGG    = "run.log"
PATHP   = "./"
FMT     = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"

class LogHandler(logging.Logger):
    """
        {"stdout":True/False,"stderr":True/False,"File":True/False}
    """
    def __init__(self, name = LOGG, path = PATHP, level = DEBUG, fmt = FMT, **kwargs):
        self.path = path
        try:
            name = os.path.splitext(name)[0]
        except Exception as e:
            print("%s %s ERROR exception:%s" % (__file__, sys._getframe().f_lineno, e))
            name = LOGG
        self.fmt = fmt
        self.name = name
        self.level = level
        super().__init__(self.name,level)
        try:
            if kwargs.get("stdout",False):
                self.__setStreamHandler__()
            if kwargs.get("File",False):
                self.__setFileHandler__()
        except Exception as e:
            print("%s %s ERROR exception:%s" % (__file__, sys._getframe().f_lineno, e))


    def __setFileHandler__(self):
        """

        :return:
        """
        fileName = os.path.join(self.path,'{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        fHandler = TimedRotatingFileHandler(filename=fileName, when='D', interval=1, backupCount=15)
        fHandler.suffix = '%Y%m%d.log'
        fHandler.setLevel(self.level)
        formatter = logging.Formatter(self.fmt)
        fHandler.setFormatter(formatter)
        self.fHandler = fHandler
        self.addHandler(fHandler)

    def __setStreamHandler__(self):
        """

        :return:
        """
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter(self.fmt)
        streamHandler.setFormatter(formatter)
        streamHandler.setLevel(self.level)
        self.addHandler(streamHandler)

    def resetLog(self,name = LOGG):
        try:
            name = os.path.splitext(name)[0]
        except Exception as e:
            print("%s %s ERROR exception:%s" % (__file__, sys._getframe().f_lineno, e))
            name = LOGG

        self.name = name
        self.removeHandler(self.fHandler)
        self.__setFileHandler__()

log = LogHandler(name='run.log',path='../logs',stdout=True,File=True)

if __name__ == '__main__':
    # log = LogHandler(name='run.log',path='../logs',stdout=True,File=True)
    log.info("msg is test...")
