#coding = utf8

'''
-------------------------------------------------
   File Name：     CrawlerProxyListplus.py
   Description :
   Author :       lf
   date：         2018/07/24
-------------------------------------------------
'''

from Spider.CrawlerProxyBase import CrawlerProxyBase
from Util.LogHandler import *
from bs4 import BeautifulSoup
import re
import sys
import urllib.parse

class CrawlerProxyListplus(CrawlerProxyBase):
    """
    继承CrawlerProxyBase   实现特定抓取函数
    数据类型：{"IP:端口":[IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间]}
    IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间
    36.67.32.87 8080 匿名 http 印度尼西亚 东爪哇XX Telin 5.639 秒 1分钟前
    """
    def __init__(self,seedUrlList=None,linksCallback=None,scrapeCallback=None,linkSorted=None,cache=None,maxDepth=-1):
        if seedUrlList is None:
            seedUrlList = [
                'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1'
            ]
        if linksCallback is None:
            linksCallback = self.linksCallback

        if scrapeCallback is None:
            scrapeCallback = self.scrapeCallback

        if linkSorted is None:
            linkSorted = self.linkSorted

        if cache is None:
            pass

        super().__init__(seedUrlList, linksCallback, scrapeCallback, linkSorted, cache, maxDepth)

    def linkSorted(self,urlList):
        sList = sorted(urlList,key=lambda x: int(x.split('-')[-1]),reverse=True)
        urlList.clear()
        urlList.extend(sList)

    def linksCallback(self, html, url=None):
        # html.encoding = 'gbk'
        html = html.text
        html = BeautifulSoup(html, "lxml")
        baseUrl = urllib.parse.urlparse(url).scheme + "://" + urllib.parse.urlparse(url).netloc
        # print(baseUrl)
        log.info('func linksCallback the base url is :{}'.format(baseUrl))

        result = []
        try:
            # x = html.find('table', {'cellspacing': '0'})
            # print(x)
            tags = html.find('table', {'cellspacing': '0'}).find_all('a',{'href':True})
            if tags is not None:
                # print(tags)
                for item in tags:
                    # print(item['href'])
                    tmp = urllib.parse.urljoin(baseUrl,item['href'])
                    if tmp in result:
                        continue
                    result.append(tmp)
        except Exception as e:
            log.error("exception:{}".format(e))
            raise Exception
        # print(result)
        return result

    def scrapeCallback(self, html):
        # html.encoding = 'utf8'
        html = html.text
        html = BeautifulSoup(html, "lxml")
        result = []
        try:
            # print(html.find('table', {'cellspacing': '1','class':'bg'}))
            tags = html.find('table', {'cellspacing': '1','class':'bg'}).find_all('tr',{'class':'cells'})
            if tags is not None:
                for item in tags:
                    # print(item)
                    lis = item.find_all('td')
                    # print(len(lis))
                    if lis is None or len(lis)==0:
                        continue
                    liValue = []
                    for li in lis:
                        if li.string is None:
                            continue
                        liValue.append(li.string)
                    # print(liValue)
                    result.append({liValue[0] + ":" + liValue[1]: liValue})
        except Exception as e:
            log.error("exception:{}".format(e))
            raise Exception
        return result

if __name__ == '__main__':
    seedUrlList = [
        'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1'
    ]
    for url in seedUrlList:
        m = CrawlerProxyListplus([url])
        m.start()

        for item in m.iteritem(1):
            print(item)
            m.stop()