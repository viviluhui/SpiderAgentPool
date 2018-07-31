#coding = utf8

'''
-------------------------------------------------
   File Name：     DbFactory.py
   Description :
   Author :       lf
   date：         2018/07/18
-------------------------------------------------
   Change Activity:
                  2016/07/18:
----
'''

__author__ = 'lf'

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Util.UtilTool import Singleton
from Util.LogHandler import *
from Util.RunParam import RunParam

class DbFactory(object):
    """
    数据库工厂类 提供各类数据库抽象方法

    抽象方法：
        get(proxy)          proxy: ip:port 返回代理信息
        put(proxy)          存入一个代理
        pop()               弹出一个代理
        exists(proxy)       判断代理是否存在
        getNumber()         返回代理总数
        delete(proxy)       删除代理
        getAll()            返回所有代理
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.m_runParam = RunParam()
        self.__initDbByConFile()

    def __initDbByConFile(self):
        __type = None
        log.info("type:{} host:{} port:{} ".format(self.m_runParam.dbType,self.m_runParam.dbHost,self.m_runParam.dbPort))
        if "SSDB" == self.m_runParam.dbType:
            __type = 'SsdbDao'
        else:
            pass
        assert __type, log.error('type error,Not support DB:{}'.format(self.m_runParam.dbType))
        self.m_dbDao = getattr(__import__(__type),__type)(host=self.m_runParam.dbHost,
                                                          port=self.m_runParam.dbPort)
        if self.m_dbDao is None:
            raise Exception

    def get(self,key,**kwargs):
        return self.m_dbDao.get(key,**kwargs)

    def gets(self,**kwargs):
        return self.m_dbDao.gets(**kwargs)

    def set(self,key,value,**kwargs):
        return self.m_dbDao.set(key,value,**kwargs)

    def sets(self,obj):
        if isinstance(obj,list):
            for itemDic in obj:
                for k,v in itemDic.items():
                # k,v = item.popitem()
                    if isinstance(v,list):
                        v = ",".join(v)
                    # tt = self.m_dbDao.exists(k)
                    # print(k,v,type(tt))
                    if self.m_dbDao.exists(k):
                        log.info("db key[{}] is exists".format(k))
                    else:
                        log.info("db key[{}] is not exists".format(k))
                        self.m_dbDao.set(key=k,value=v)

    def pop(self,DeF=False,**kwargs):
        return self.m_dbDao.pop(DeF)

    # def update(self,key,value,**kwargs):
    #     return self.m_dbDao.update(key,value,**kwargs)
    #
    # def updates(self,obj):
    #     if isinstance(obj,list):
    #         for item in obj:
    #             print(item)
    #             k,v = item.popitem()
    #             self.m_dbDao.update(key=k,value=v)

    def delete(self,key,**kwargs):
        return self.m_dbDao.delete(key, **kwargs)

    def exists(self,key,**kwargs):
        return self.m_dbDao.exists(key, **kwargs)

    def getAll(self,**kwargs):
        return self.m_dbDao.getAll(**kwargs)

    def getProxyCount(self,**kwargs):
        return self.m_dbDao.getAll(**kwargs)

    def chgHashName(self, name, **kwargs):
        return self.m_dbDao.chgHashName(name)

if __name__ == '__main__':
    db = DbFactory()
    print(db.getAll())
