#coding = utf8

'''
-------------------------------------------------
   File Name：     CrawlerProxy181ip.py
   Description :
   Author :       lf
   date：         2018/07/24
-------------------------------------------------
'''

from Spider.CrawlerProxyBase import CrawlerProxyBase
from Util.LogHandler import *
from bs4 import BeautifulSoup
import json
import sys

class CrawlerProxy181ip(CrawlerProxyBase):
    """
    继承CrawlerProxyBase   实现特定抓取函数
    数据类型：{"IP:端口":[IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间]}
    IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间
    36.67.32.87 8080 匿名 http 印度尼西亚 东爪哇XX Telin 5.639 秒 1分钟前
    """
    def __init__(self,seedUrlList=None,linksCallback=None,scrapeCallback=None, linkSorted=None, cache=None,maxDepth=-1):
        if seedUrlList is None:
            seedUrlList = [
                'http://www.ip181.com/'
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
        # html.encoding = 'gbk'
        jsonDict = html.json()
        # print(html)
        result = []
        try:
            # print(type(json_text))
            # print("-----")
            rCode = jsonDict['ERRORCODE']
            res = jsonDict['RESULT']

            for item in res:
                ip = item['ip']
                port = item['port']
                position = item['position']
                liValue = [ip,port,'','',position,'','','']
                result.append({ip + ":" + port: liValue})

            # for k,v in jsonDict.items():
            #     print(k,v)
        except Exception as e:
            log.error("exception:{}".format(e))
            raise Exception
        return result

if __name__ == '__main__':
    m = CrawlerProxy181ip()
    m.start()

    for item in m.iteritem(1):
        print(item)
        m.stop()