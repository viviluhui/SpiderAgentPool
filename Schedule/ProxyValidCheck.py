#coding = utf8
'''
-------------------------------------------------
   File Name：     ProxyValidSchedule.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''

import sys
import os
import time
from threading import Thread
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Util.UtilTool import validUsefulProxy
from Util.UtilTool import validNetWork
from Cache.DbCache import Catch
from Util.LogHandler import *

MAXFCNT = 5
class ProxyVaildCheck(Thread):

    def __init__(self,queue,proxysDict,index):
        Thread.__init__(self)
        self.queue = queue
        self.cache = Catch()
        self.proxysDict = proxysDict
        self.index = index
        self.iFailedCount = MAXFCNT

    def run(self):
        while self.queue.qsize():
            start = time.clock()
            proxy = self.queue.get()
            if isinstance(proxy,bytes):
                proxy = proxy.decode('utf8')
            if validUsefulProxy(proxy):
                log.info('ProxyVaildCheck{}: {} validation pass'.format(self.index,proxy))
                # log.info("starting delete from db [{}]".format(self.m_runParam.dbChkName))
                # self.db.chgHashName(self.m_runParam.dbChkName)
                # self.db.delete(proxy)
                # log.info("starting set into db [{}]".format(self.m_runParam.dbUsrName))
                # self.db.chgHashName(self.m_runParam.dbUsrName)
                # self.db.set(proxy,self.proxysDict[proxy.encode('utf8')])
                self.iFailedCount = MAXFCNT
            else:
                # self.deleteProxy(proxy)
                log.info('ProxyVaildCheck{}: {} validation fail'.format(self.index, proxy))
                # log.info("starting delete from db [{}]".format(self.m_runParam.dbUsrName))
                # self.db.chgHashName(self.m_runParam.dbUsrName)
                # self.db.delete(proxy)
                self.cache.deleteProxy(proxy)
                self.iFailedCount -= 1
                if self.iFailedCount <= 0:
                    try:
                        validNetWork()
                        self.iFailedCount = MAXFCNT
                        log.info("网络正常....")
                    except Exception as e:
                        self.queue.queue.clear()
                        log.error("网络异常....")

            end = time.clock()
            log.info('run time {}'.format(end-start))
            self.queue.task_done()