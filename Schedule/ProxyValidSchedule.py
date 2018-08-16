#coding = utf8
'''
-------------------------------------------------
   File Name：     ProxyValidSchedule.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
            线程版本  代理有效性检查
'''

import sys
import os
import time
from queue import Queue
from apscheduler.schedulers.blocking import BlockingScheduler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Schedule.ProxyValidCheck import ProxyVaildCheck
from Util.RunParam import RunParam
from Util.UtilTool import validNetWork
from Util.LogHandler import *
from Db.DbFactory import DbFactory

class ProxyValidSchedule(object):
    def __init__(self):
        self.queue = Queue()
        self.db = DbFactory()
        self.m_runParam = RunParam()
        self.proxys = None

    def __ProxyVaildCheckThread(self):
        threadList = list()
        for index in range(10):
            threadList.append(ProxyVaildCheck(self.queue,self.proxys,index))

        for item in threadList:
            item.setDaemon(True)
            item.start()

        for item in threadList:
            item.join()

    def run(self):
        self.putsQueue()

        while True:
            if not self.queue.empty():
                print("Start valid useful proxy")
                self.__ProxyVaildCheckThread()
            # else:
            #     sleepTime = 60 * 5
            #     print('Valid Complete! sleep {} seconds.'.format(sleepTime))
            #     time.sleep(sleepTime)
            #     self.putsQueue()
            else:
                break

            # time.sleep(120)

    def putsQueue(self):
        """

        :return:
        """
        self.db.chgHashName(self.m_runParam.dbUsrName)
        # proxys = self.db.gets()
        self.proxys = self.db.getAll()
        # print(type(self.proxys))
        for k,v in self.proxys.items():
            self.queue.put(k)

def mainRun():
    try:
        validNetWork()
        log.info("网络正常....")
    except Exception as e:
        log.error("网络异常....")
        return
    p = ProxyValidSchedule()
    p.run()

def run():
    # p = ProxyValidSchedule()
    # p.run()
    mainRun()
    sch = BlockingScheduler()
    sch.add_job(mainRun, "interval", minutes=5)
    sch.start()


if __name__ == '__main__':
    run()