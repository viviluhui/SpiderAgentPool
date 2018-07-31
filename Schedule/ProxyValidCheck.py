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
from Util.RunParam import RunParam
from Db.DbFactory import DbFactory
from Util.LogHandler import *

class ProxyVaildCheck(Thread):

    def __init__(self,queue,proxysDict,index):
        Thread.__init__(self)
        self.queue = queue
        self.db = DbFactory()
        self.m_runParam = RunParam()
        self.proxysDict = proxysDict
        self.index = index

    def run(self):
        while self.queue.qsize():
            start = time.clock()
            proxy = self.queue.get()
            if isinstance(proxy,bytes):
                proxy = proxy.decode('utf8')
            if validUsefulProxy(proxy):
                log.info('ProxyVaildCheck{}: {} validation pass'.format(self.index,proxy))
                log.info("starting delete from db [{}]".format(self.m_runParam.dbChkName))
                self.db.chgHashName(self.m_runParam.dbChkName)
                self.db.delete(proxy)
                log.info("starting set into db [{}]".format(self.m_runParam.dbUsrName))
                self.db.chgHashName(self.m_runParam.dbUsrName)
                self.db.set(proxy,self.proxysDict[proxy.encode('utf8')])
            else:
                # self.deleteProxy(proxy)
                log.info('ProxyVaildCheck{}: {} validation fail'.format(self.index, proxy))
                log.info("starting delete from db [{}]".format(self.m_runParam.dbChkName))
                self.db.chgHashName(self.m_runParam.dbChkName)
                self.db.delete(proxy)

            end = time.clock()
            log.error('run time {}'.format(end-start))
            self.queue.task_done()