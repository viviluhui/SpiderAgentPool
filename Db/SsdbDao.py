#coding = utf8

'''
-------------------------------------------------
   File Name：     SsdbDao.py
   Description :
   Author :       lf
   date：         2018/07/18
-------------------------------------------------
   Change Activity:
                  2018/07/18:   init
                  2018/08/15:   取消所有打印，独立模块
----
'''

__author__ = 'lf'

import pyssdb
import random

class SsdbDao(object):
    """
        SSDB数据库接口
        代理存放的容器为hash:
            原始代理存放在name为rawProxy的hash中，key为代理的ip:port,value为None
            验证后的代理存放在name为useProxy的hash中,key为代理的ip:port,value为计数，初始为1，每校验失败一次减1；成功一次加1
    """
    name = ""


    def __init__(self, host, port):
        """
        init
        :param host: ssdb host ip
        :param port: ssdb host port
        :return
        """
        try:
            self.__conn = pyssdb.Client(host, int(port))
        except Exception as e:
            self.__conn = None
            raise e


    def __del__(self):
        if self.__conn is not None and hasattr(self.__conn, 'disconnect'):
            self.__conn.disconnect()


    def get(self, key):
        """
        从hash中获取对应的proxy，使用chngHashName修改指定hash name,
        :param proxy:
        :param name:
        :return:
        """
        try:
            return self.__conn.hget(self.name, key)
        except Exception as e:
            raise e


    def gets(self, num=100):
        """
            获取一批代理
        :param num:
        :return:	dict {proxy:value}
        """
        try:
            return self.__conn.hkeys(self.name, "", "", num)
        except Exception as e:
            raise e


    def set(self, key, value):
        """
        将代理放入hash,使用chngHashName修改指定hash name,
        :param proxy:
        :param value:
        :return:
        """
        try:
            self.__conn.hset(self.name, key, value)
        except Exception as e:
            raise e


    def delete(self, key):
        """
        将代理从hash删除,使用chngHashName修改指定hash name,
        :param key:
        :param name:
        :return:
        """
        try:
            self.__conn.hdel(self.name, key)
        except Exception as e:
            raise e


    # def update(self,key,value):
    #     """
    #     更新代理,使用chngHashName修改指定hash name,
    #     :param key:
    #     :param value:
    #     :param name:
    #     :return:
    #     """
    #     try:
    #         self.__conn.hincrby(self.name,key,value)
    #     except Exception as e:
    #         log.error("exception:{}".format(e))

    def pop(self, seq=False, isDelete=False):
        """
            弹出一条数据
        :param name:
        :return: dict {proxy:value}
        """
        try:
            if seq:
                key = self.__conn.hscan(self.name, "", "", 1)
            else:
                key = self.__conn.hrscan(self.name, "", "", 1)
            if key is not None:
                if isDelete:
                    self.delete(key)

                value = self.__conn.hget(self.name, key)
                return {'key': key, 'value': value}
        except Exception as e:
            raise e


    def random(self, seed=100, isDelete=False):
        """
            随机弹出一个代理
        :param name:
        :return: dict {proxy:value}
        """
        try:
            proxys = self.__conn.hkeys(self.name, "", "", seed)
            if proxys is not None:
                # log(proxys)
                proxy = random.choice(proxys)
                value = self.__conn.hget(self.name, proxy)
                if isDelete:
                    self.delete(proxy)
                return {'key': proxy, 'value': value}
        except Exception as e:
            raise e


    def exists(self, key):
        """

        :param key:
        :param name:
        :return:
        """
        try:
            return int(self.__conn.hexists(self.name, key).decode('utf8'))
        except Exception as e:
            raise e


    def getAll(self):
        """

        :param name:
        :return:
        """
        try:
            items = self.__conn.hgetall(self.name)
            itemDict = dict()
            for i in range(0, len(items), 2):
                itemDict[items[i]] = items[i + 1]
            return itemDict
        except Exception as e:
            raise e


    def getCount(self):
        """

        :param name:
        :return:
        """
        try:
            return self.__conn.hlen(self.name)
        except Exception as e:
            raise e


    def chgHashName(self, name):
        """

        :param name:
        :return:
        """
        self.name = name

if __name__ == '__main__':
    RAW = "rawproxy"
    USR = "useproxy"
    CHK = "chkproxy"
    host = '192.168.179.130'
    port = 8888
    m = SsdbDao(host,port)
    m.chgHashName(RAW)
    # m.put("127.0.0.1:80")
    # m.put("127.0.0.1:80",value=0,name=RAW)
    items = m.getAll()

    for i in range(0,len(items),2):
        print(items[i],items[i+1])
        m.chgHashName(CHK)
        m.set(items[i],items[i+1])
