#coding = utf8

'''
-------------------------------------------------
   File Name：     SpiderFactory.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Util.UtilTool import Singleton

class SpiderFactory(object):
    """
    工厂类 提供各类网站爬虫抽象方法

    抽象方法:

    start(spn=)             开始爬虫,iteritem模式时控制
    stop(spn=)              停止爬虫,iteritem模式时控制
    iteritem(spn,)          生成器返回抓取代理结果


    itemWriter(spn,writer)  代理结果写入

    数据类型：
    IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间
    36.67.32.87 8080 匿名 http 印度尼西亚 东爪哇XX Telin 5.639 秒 1分钟前
    """
    # __metaclass__ = Singleton

    def __init__(self,spiderName,seedUrlList=None,cache=None):
        # print(seedUrlList)
        self.name = spiderName
        self.__splider = getattr(__import__(spiderName), spiderName)(seedUrlList,cache=cache)
        if self.__splider is None:
            raise Exception

    def start(self):
        self.__splider.start()

    def stop(self):
        self.__splider.stop()

    def iteritem(self,intervalTime=1):
        return self.__splider.iteritem(intervalTime)

    def itemWriter(self,writer=None,page=-1):
        self.__splider.itemWriter(writer,page=page)