#coding = utf8

'''
-------------------------------------------------
   File Name：     DbCache.py
   Description :    调用DbFactory接口,数据库缓存类
   Author :       lf
   date：         2018/08/15
-------------------------------------------------
'''

from Util.LogHandler import *
from Util.RunParam import RunParam
from Db.DbFactory import DbFactory

class Catch(object):

    def __init__(self):
        self.db = DbFactory()
        self.m_runParam = RunParam()

    def write(self,proxys):
        log.info("starting sets into db [{}]".format(self.m_runParam.dbRawName))
        self.db.chgHashName(self.m_runParam.dbRawName)
        self.db.sets(proxys)
        log.info("starting sets into db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        self.db.sets(proxys)

    def popProxy(self, isDelete=False):
        """
        #获取代理
        :param DeF: 弹出后是否删除标志
        :return:
        """
        log.info("starting pop from db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        # self.db.chgHashName(self.m_runParam.dbRawName)
        return self.db.random(isDelete=isDelete)


    def deleteProxy(self, proxy):
        """
        #删除代理
        :param proxy:
        :return:
        """
        log.info("starting delete from db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        # self.db.chgHashName(self.m_runParam.dbRawName)
        self.db.delete(proxy)


    def getProxy(self, key):
        """
        #获取代理
        :return:
        """
        log.info("starting delete from db [{}]".format(self.m_runParam.dbUsrName))
        self.db.chgHashName(self.m_runParam.dbUsrName)
        # self.db.chgHashName(self.m_runParam.dbRawName)
        self.db.get(key)