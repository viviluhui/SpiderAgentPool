#coding = utf8

'''
-------------------------------------------------
   File Name：     CrawlerProxy5u.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
------------------2018/08/15    __runFlag 目前无法立即停止itemWriter，程序内部变量，无法异步修改
'''


from bs4 import BeautifulSoup
import urllib
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web.RequestWeb import *
from Util.LogHandler import *

class CrawlerProxyBase(object):
    """
    爬虫基类，定义所有爬虫功能  抓取数据由回调函数scrapeCallback、linksCallback完成
    """
    def __init__(self,seedUrlList,linksCallback=None,scrapeCallback=None,linkSorted=None,cache=None,maxDepth=-1):
        self.__runFlag = True
        #初始爬虫网址
        if isinstance(seedUrlList,str):
            # print(seedUrlList)
            self.crawlQueue = [seedUrlList]
            self.seedQueue = None
            self.__crawlQueue = [seedUrlList]
            self.__seedQueue = None
        else:
            self.crawlQueue = [seedUrlList[0]]
            #爬虫种子地址,爬虫运行总是从初始爬虫网址开始，调用回调函数会添加超链接到crawlQueue,当crawlQueue为none时，从seedQueue添加一个到crawQueue
            self.seedQueue = seedUrlList[:]

            self.__crawlQueue = [seedUrlList[0]]
            self.__seedQueue = seedUrlList[:]

        log.info("crawler seedQueue is :{}".format(self.seedQueue))

        #已成功爬取网址
        self.crawlSeenDic = {}
        #设置初始爬取网址深度为0
        # for url in self.crawlQueue:
        #     self.crawlSeenDic.setdefault(url,0)
        #回调函数  网页有效超链接获取函数  输入url对应网页内容  返回列表
        self.funcLinksCallBck = linksCallback

        #回调函数 网页内容获取
        self.funcScrapeCallBck = scrapeCallback

        #回调函数 对crawlQueue进行排序
        self.linkSorted = linkSorted

        #maxDepth访问页面最大次数 maxDepth设置为负数，取消限制
        self.maxDepth = maxDepth

        #回调函数，存储数据
        self.cache = cache
        super().__init__()

    def start(self):
        """

        :return:
        """
        self.__runFlag = True

    def restart(self):
        """

        :return:
        """
        self.stop()
        self.crawlQueue.clear()
        self.crawlQueue = self.__crawlQueue[:]
        self.seedQueue = self.__seedQueue[:]

        self.start()


    def stop(self):
        """

        :return:
        """
        self.__runFlag = False
        self.crawlQueue.clear()


    def iteritem(self,intervalTime=1):
        """

        :param intervalTime:    interval time request web
        :return:
        """
        while self.crawlQueue:
            #运行标志
            if not self.__runFlag :
                break
            #网址遇见最大次数
            if self.maxDepth > 0 and self.crawlSeenDic[url] > self.maxDepth:
                break

            url = self.crawlQueue.pop()
            baseurl = url
            # baseurl = urllib.parse.urlparse(seed_url).scheme + "://" + urllib.parse.urlparse(seed_url).netloc
            log.info("crawler url is :{}".format(url))

            ###获取网页内容
            res = web(url)
            if res is None:
                log.error("network error")
                break
            self.crawlSeenDic[url] = self.crawlSeenDic.setdefault(url,0) + 1

            #调用回调函数获取网页有效链接
            links = []
            if self.funcLinksCallBck:
                links.extend(self.funcLinksCallBck(res, url) or [])

            for link in links:
                # link = urllib.parse.urljoin(baseurl,link)
                if link not in self.crawlSeenDic:
                    self.crawlSeenDic.setdefault(link,0)
                    self.crawlQueue.append(link)

            if self.linkSorted:
                self.linkSorted(self.crawlQueue)

            # print(self.crawlQueue)

            if self.funcScrapeCallBck:
                try:
                    yield self.funcScrapeCallBck(res)
                except Exception as e:
                    log.error("exception:{}".format(e))
                    raise Exception

            time.sleep(intervalTime)

            if len(self.crawlQueue)==0 and self.seedQueue is not None and len(self.seedQueue)>0:
                self.crawlQueue.append(self.seedQueue.pop())

    def itemWriter(self,cache=None,page=-1,intervalTime=1):
        """

        :param cache:       数据存储协议 输入
        :param page:        从seed开始爬取最大网址数量 负数表示不限制
        :param intervalTime:
        :return:    返回抓取数据量
        """
        count = 0
        __page = page
        while self.crawlQueue:
            # 运行标志
            if not self.__runFlag:
                break
            # 网址遇见最大次数
            if self.maxDepth > 0 and self.crawlSeenDic[url] > self.maxDepth:
                break

            url = self.crawlQueue.pop()
            baseurl = url
            # baseurl = urllib.parse.urlparse(seed_url).scheme + "://" + urllib.parse.urlparse(seed_url).netloc
            log.info("crawler url is :{}".format(url))

            ###获取网页内容
            res = web(url)
            if res is None:
                log.error("network error")
                break
            self.crawlSeenDic[url] = self.crawlSeenDic.setdefault(url, 0) + 1

            # 调用回调函数获取网页有效链接
            links = []
            if self.funcLinksCallBck:
                links.extend(self.funcLinksCallBck(res, url) or [])

            for link in links:
                # link = urllib.parse.urljoin(baseurl,link)
                if link not in self.crawlSeenDic:
                    self.crawlSeenDic.setdefault(link, 0)
                    self.crawlQueue.append(link)

            if self.linkSorted:
                self.linkSorted(self.crawlQueue)

            # print(self.crawlQueue)

            if self.funcScrapeCallBck:
                try:
                    result = self.funcScrapeCallBck(res)
                    log.info("funcScrapeCallBck value:{}".format(result))
                    count += len(result)
                    if self.cache:
                        self.cache.write(result)
                except Exception as e:
                    log.error("exception:{}".format(e))
                    raise Exception

            time.sleep(intervalTime)

            if __page>0:
                page -= 1
                if page <= 0:
                    self.crawlQueue.clear()
                    page = __page

            if len(self.crawlQueue) == 0 and self.seedQueue is not None and len(self.seedQueue) > 0:
                self.crawlQueue.append(self.seedQueue.pop())

        return count

if __name__ == '__main__':
    urlList = [
        'http://www.data5u.com/free/index.shtml',
        'http://www.data5u.com/free/gngn/index.shtml',
        'http://www.data5u.com/free/gnpt/index.shtml',
        'http://www.data5u.com/free/gwgn/index.shtml',
        'http://www.data5u.com/free/gwpt/index.shtml'
    ]
    m = CrawlerProxyBase(urlList)
    m.start()

    for item in m.iteritem(30):
        print(item)
        m.stop()