#coding = utf8

'''
-------------------------------------------------
   File Name：     DbFactory.py
   Description :
   Author :       lf
   date：         2018/07/18
-------------------------------------------------
   Change Activity:
                  2018/07/18:   init
                  2018/08/15:   去除LogHandler模块打印，此模块更独立，移植方便
                                修改pop为从表首或进表尾取数
                                增加random随机取数
----
'''

__author__ = 'lf'

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Util.UtilTool import Singleton
from Util.RunParam import RunParam

class DbFactory(object):
    """
    数据库工厂类 提供各类数据库抽象方法

    抽象方法：
        get(proxy)          proxy: ip:port 返回代理信息
        put(proxy)          存入一个代理
        pop()               弹出一个代理
        exists(proxy)       判断代理是否存在
        delete(proxy)       删除代理
        getAll()            返回所有代理
    """
    __metaclass__ = Singleton

    connInfo = None

    def __init__(self):
        self.m_runParam = RunParam()
        self.__initDbByConFile()


    def __initDbByConFile(self):
        __type = None
        self.connInfo = "type:{} host:{} port:{} ".format(self.m_runParam.dbType, self.m_runParam.dbHost,
                                                          self.m_runParam.dbPort)

        if "SSDB" == self.m_runParam.dbType:
            __type = 'SsdbDao'
        else:
            pass
        assert __type, 'type error,Not support DB:{}'.format(self.m_runParam.dbType)
        self.m_dbDao = getattr(__import__(__type), __type)(host=self.m_runParam.dbHost,
                                                           port=self.m_runParam.dbPort)
        if self.m_dbDao is None:
            raise Exception


    def get(self, key, **kwargs):
        """
            根据key值获取数据
        :param key:
        :param kwargs:
        :return:
        """
        return self.m_dbDao.get(key, **kwargs)


    def gets(self, num, **kwargs):
        """
            获取一批数据
        :param num:
        :param kwargs:
        :return:
        """
        return self.m_dbDao.gets(num, **kwargs)


    def set(self, key, value, **kwargs):
        """
            插入数据,相同key数据替换
        :param key:
        :param value:
        :param kwargs:
        :return:
        """
        return self.m_dbDao.set(key, value, **kwargs)


    def sets(self, obj, up=False):
        """
            批量插入数据
        :param obj: obj为list的字典   [{k:v},{k:v}]
        :param up:  相同数据操作方式   true覆盖  false丢弃
        :return:
        """
        if isinstance(obj, list):
            for itemDic in obj:
                for k, v in itemDic.items():
                    if isinstance(v, list):
                        v = ",".join(v)
                    else:
                        try:
                            # 尝试强制将其转为str
                            v = str(v)
                        except Exception as e:
                            raise e

                    if up and self.m_dbDao.exists(k):
                        self.m_dbDao.set(key=k, value=v)
                    else:
                        self.m_dbDao.set(key=k, value=v)


    def pop(self, seq=False, isDelete=False, **kwargs):
        """
            弹出一条数据
        :param seq:     弹出数据顺序
        :param kwargs:
        :return:        {key:"",value:""}
        """
        return self.m_dbDao.pop(seq, isDelete)


    def random(self, seed=100, isDelete=False):
        """
            随机弹出一条数据
        :param seed:    弹出数据范围
        :param isDelete:
        :return:    {key:"",value:""}
        """
        return self.m_dbDao.random(seed, isDelete)


    def delete(self, key, **kwargs):
        """
            删除数据
        :param key:
        :param kwargs:
        :return:
        """
        return self.m_dbDao.delete(key, **kwargs)


    def exists(self, key, **kwargs):
        """

        :param key:
        :param kwargs:
        :return:
        """
        return self.m_dbDao.exists(key, **kwargs)


    def getAll(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.m_dbDao.getAll(**kwargs)


    def getCount(self, **kwargs):
        """
            获取数据总量
        :param kwargs:
        :return:
        """
        return self.m_dbDao.getCount(**kwargs)


    def chgHashName(self, name, **kwargs):
        """

        :param name:
        :param kwargs:
        :return:
        """
        return self.m_dbDao.chgHashName(name)

if __name__ == '__main__':
    db = DbFactory()
    print(db.getAll())
