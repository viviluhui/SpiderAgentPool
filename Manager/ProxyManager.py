#coding = utf8

'''
-------------------------------------------------
   File Name：     ProxyGain.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''

import sys
import os
from Spider.SpiderFactory import SpiderFactory
from Util.UtilTool import Singleton
from Util.RunParam import RunParam
from Util.LogHandler import *
from Db.DbFactory import DbFactory

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ProxyManager(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.__splider = {}
        self.db = DbFactory()
        self.m_runParam = RunParam()
        self.__initSplider()
        # self.__page = int(self.m_runParam.proxyPage)

    def __initSplider(self):
        """

        :return:
        """
        for proxyGetter,v in self.m_runParam.proxyGetterDict:
            try:
                self.add(proxyGetter.strip(),proxyGetter.strip(),v.split(','),self)
            except Exception as e:
                log.error("exception:{}".format(e))

    # def __isRunControl(self):
    #     if self.m_runParam.proxyMode == 'u':
    #         if self.__page <= 0:
    #             return False
    #         else:
    #             return True
    #         self.__page -= 1
    #     elif self.m_runParam.proxyMode == 'a':
    #         return True
    #     elif self.m_runParam.proxyMode == 'i':
    #         pass
    #     else:
    #         return False


    def write(self,proxys):
        log.info("starting sets into db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        self.db.sets(proxys)
        log.info("starting sets into db [{}]".format(self.m_runParam.dbChkName))
        self.db.chgHashName(self.m_runParam.dbChkName)
        self.db.sets(proxys)


    def pop(self,key):
        return self.__splider.pop(key)

    def add(self, key, spiderName,url=None,cache=None):
        """
        根据类名动态添加爬虫对象到列表
        :param key:
        :param spiderName:
        :return:
        """
        mSplider = SpiderFactory(spiderName,seedUrlList=url,cache=cache)
        self.__splider[key] = mSplider

    def iterSpider(self):
        for k,proxy in self.__splider.items():
            yield proxy

    def refreshProxy(self, proxy):
        """

        :param proxy:
        :return:
        """
        log.info("starting write date to db [{}]".format(self.m_runParam.dbRawName))
        self.db.chgHashName(self.m_runParam.dbRawName)

        log.info("{func}: fetch proxy start".format(func=proxy.name))
        ####1
        # for item in proxy.iteritem(1):
        #     log.info("the value:{}".format(item))
        #     self.db.sets(item)
        #     item.stop if pg == 0 else pg -= 1
        proxy.itemWriter(page=int(self.m_runParam.proxyPage))
        log.info("{func}: fetch proxy end  ".format(func=proxy.name))

    def refreshAllProxy(self):
        """
        所有爬虫zawqrsxz
        :return:
        """
        log.info("starting write date to db [{}]".format(self.m_runParam.dbRawName))
        self.db.chgHashName(self.m_runParam.dbRawName)
        # self.db.chgHashName("test")

        for k,proxy in self.__splider.items():
            log.info("{func}: fetch proxy start".format(func=proxy.name))
            proxy.itemWriter(page=int(self.m_runParam.proxyPage))
            # for item in proxy.iteritem(1):
            #     log.info("the value:{}".format(item))
            #     self.db.sets(item)
            #     proxy.stop()
            #     if pg == 0:
            #         proxy.stop()
            #     else:
            #         pg -= 1
            log.info("{func}: fetch proxy end  ".format(func=proxy.name))


    def popProxy(self,DeF=False):
        """
        #获取代理
        :param DeF: 弹出后是否删除标志
        :return:
        """
        log.info("starting pop from db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        # self.db.chgHashName(self.m_runParam.dbRawName)
        return self.db.pop(DeF)

    def deleteProxy(self,proxy):
        """
        #删除代理
        :param proxy:
        :return:
        """
        log.info("starting delete from db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        # self.db.chgHashName(self.m_runParam.dbRawName)
        self.db.delete(proxy)

    def getProxy(self,key):
        """
        #获取代理
        :return:
        """
        log.info("starting delete from db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        # self.db.chgHashName(self.m_runParam.dbRawName)
        self.db.get(key)

if __name__ == "__main__":
    m = ProxyManager()
    m.refreshAllProxy()
    log.info(m.pop())
