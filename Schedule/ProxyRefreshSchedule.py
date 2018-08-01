#coding = utf8
'''
-------------------------------------------------
   File Name：     ProxyRefreshSchedule.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''

import sys
import os
import time
from Util.RunParam import RunParam
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler
from Manager.ProxyManager import ProxyManager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def refreshPool(p,proxy):
    print(proxy.name)
    p.refreshProxy(proxy)

def gProxyRefresh():
    p = ProxyManager()

    pl = []
    for item in p.iterSpider():
        proc = Thread(target=refreshPool,args=(p,item))
        pl.append(proc)
        proc.setDaemon(True)        #设置线程为后台线程，前台线程结束，后台线程立即结束
        proc.start()

    for proc in pl:
        proc.join()

def uProxyRefresh():
    p = ProxyManager()

    pl = []
    for item in p.iterSpider():
        proc = Thread(target=refreshPool,args=(p,item))
        pl.append(proc)
        proc.setDaemon(True)        #设置线程为后台线程，前台线程结束，后台线程立即结束
        proc.start()

    for proc in pl:
        proc.join()

def run():
    uProxyRefresh()
    sch = BlockingScheduler()
    sch.add_job(uProxyRefresh,"interval",minutes=10)
    sch.start()

if __name__ == '__main__':
    run()


