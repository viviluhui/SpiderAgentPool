#coding = utf8

'''
-------------------------------------------------
   File Name：     ProxyGain.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''

from Spider.SpiderFactory import SpiderFactory
from Util.UtilTool import Singleton
from Util.RunParam import RunParam
from Util.LogHandler import *
from Cache.DbCache import Catch
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ProxyManager(object):

    __metaclass__ = Singleton

    def __init__(self):
        """
            self.__splider      {
                                    spider:{    spider:class,       爬虫对象
                                                status:True/False,  爬虫状态
                                                runTime:second,     爬虫运行时间
                                                stime:,             爬虫开始运行时间
                                                etime:,             爬虫结束运行时间
                                                count,              上次爬取结果数量
                                                total,              爬取总结果数量
                                           }
                                }
        """
        self.__splider = {}
        self.catch = Catch()
        self.m_runParam = RunParam()
        self.__initSplider()
        # self.__page = int(self.m_runParam.proxyPage)

    def __initSplider(self):
        """

        :return:
        """
        for proxyGetter,v in self.m_runParam.proxyGetterDict:
            try:
                self.add(key=proxyGetter.strip(),spiderName=proxyGetter.strip(),url=v.split(','),cache=self.catch)
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
        m = {}
        m['spider'] = mSplider
        m['status'] = True
        m['runTime'] = time.strftime("%Y%m%d%H%M%S")
        m['stime'] = time.strftime("%Y%m%d%H%M%S")
        m['etime'] = time.strftime("%Y%m%d%H%M%S")
        m['count'] = 0
        m['total'] = 0

        self.__splider[key] = m

    def restartSpider(self):
        """
            爬虫运行结束后
        :return:
        """
        for k,proxy in self.__splider.items():
            proxy['spider'].restart()

    def iterSpider(self):
        for k,proxy in self.__splider.items():
            yield proxy

    def refreshProxy(self, proxy):
        """
            根据代理爬虫类更新数据
        :param proxy:
        :return:
        """
        log.info("{func}: fetch proxy start".format(func=proxy['spider'].name))
        try:
            n = proxy['spider'].itemWriter(page=int(self.m_runParam.proxyPage))
        except Exception as e:
            n = 0
            log.error("proxy refresh error")
        log.info("{func}: fetch proxy end  ".format(func=proxy['spider'].name))
        proxy['stime'] = time.strftime("%Y%m%d%H%M%S")
        proxy['etime'] = time.strftime("%Y%m%d%H%M%S")
        proxy['count'] = n
        proxy['total'] += n

    def refreshAllProxy(self):
        """
        所有爬虫
        :return:
        """
        for k,proxy in self.__splider.items():
            log.info("{func}: fetch proxy start".format(func=proxy['spider'].name))
            n = proxy['spider'].itemWriter(page=int(self.m_runParam.proxyPage))
            log.info("{func}: fetch proxy end  ".format(func=proxy['spider'].name))
            proxy['stime'] = time.strftime("%Y%m%d%H%M%S")
            proxy['etime'] = time.strftime("%Y%m%d%H%M%S")
            proxy['count'] = n
            proxy['total'] += n

    def getSplider(self):
        return self.__splider

if __name__ == "__main__":
    m = ProxyManager()
    m.refreshAllProxy()