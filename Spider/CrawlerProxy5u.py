#coding = utf8

'''
-------------------------------------------------
   File Name：     CrawlerProxy5u.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''

from Spider.CrawlerProxyBase import CrawlerProxyBase
from Util.LogHandler import *
from bs4 import BeautifulSoup


class CrawlerProxy5u(CrawlerProxyBase):
    """
    继承CrawlerProxyBase   实现特定抓取函数
    数据类型：{"IP:端口":[IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间]}
    IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间
    36.67.32.87 8080 匿名 http 印度尼西亚 东爪哇XX Telin 5.639 秒 1分钟前
    """
    def __init__(self,seedUrlList=None,linksCallback=None,scrapeCallback=None, linkSorted=None, cache=None, maxDepth=-1):

        if seedUrlList is None:
            seedUrlList = [
                'http://www.data5u.com/free/index.shtml',
                'http://www.data5u.com/free/gngn/index.shtml',
                'http://www.data5u.com/free/gnpt/index.shtml',
                'http://www.data5u.com/free/gwgn/index.shtml',
                'http://www.data5u.com/free/gwpt/index.shtml'
            ]
        if linksCallback is None:
            linksCallback = self.linksCallback

        if scrapeCallback is None:
            scrapeCallback = self.scrapeCallback

        if cache is None:
            pass

        super().__init__(seedUrlList, linksCallback, scrapeCallback, linkSorted, cache, maxDepth)

    def linksCallback(self, html, url=None):
        pass

    def scrapeCallback(self, html):
        html = html.text
        html = BeautifulSoup(html, "lxml")
        # print(html)
        result = []
        try:
            tags = html.find_all('ul', {'class': 'l2'})
            if tags is not None:
                for item in tags:
                    # print(item)
                    lis = item.find_all('li')
                    # liValue = [li.string for li in lis ]
                    # for li in lis:
                    #     liValue.append(li.string)
                    liValue = list(map(lambda x: x.string if x.string is not None else "",lis))
                    # print(liValue)
                    result.append({liValue[0] + ":" + liValue[1]: liValue})
        except Exception as e:
            log.error("exception:{}".format(e))
            raise Exception
        return result

if __name__ == '__main__':
    m = CrawlerProxy5u()
    m.start()

    for item in m.iteritem(30):
        print(item)
        m.stop()