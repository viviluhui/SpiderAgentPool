#coding = utf8
'''
-------------------------------------------------
   File Name：     main.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''

import sys
import os
from multiprocessing import Process

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Api.ProxyApi import run as ProxyApiRun
from Schedule.ProxyRefreshSchedule import run as RefreshRun
from Schedule.ProxyValidSchedule import run as ValidRun

def run():
    pList = list()


    p1 = Process(target=ProxyApiRun, name='ProxyApiRun')
    pList.append(p1)
    p2 = Process(target=ValidRun, name='ValidRun')
    pList.append(p2)
    p3 = Process(target=RefreshRun, name='RefreshRun')
    pList.append(p3)

    for p in pList:
        p.daemon = True
        p.start()
    for p in pList:
        p.join()

if __name__ == '__main__':
    run()