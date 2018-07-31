#coding = utf8

'''
-------------------------------------------------
   File Name：     CrawlerProxy66ip.py
   Description :
   Author :       lf
   date：         2018/07/24
-------------------------------------------------
'''

from Spider.CrawlerProxyBase import CrawlerProxyBase
from Util.LogHandler import *
from bs4 import BeautifulSoup
import urllib.parse
import re
import sys

class CrawlerProxy66ip(CrawlerProxyBase):
    """
    继承CrawlerProxyBase   实现特定抓取函数
    数据类型：{"IP:端口":[IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间]}
    IP 端口 匿名度 类型 国家 省市 运营商 响应速度 最后验证时间
    36.67.32.87 8080 匿名 http 印度尼西亚 东爪哇XX Telin 5.639 秒 1分钟前
    """
    def __init__(self,seedUrlList=None,linksCallback=None,scrapeCallback=None,linkSorted=None, cache=None,maxDepth=-1):
        if seedUrlList is None:
            seedUrlList = [
                'http://www.66ip.cn/'
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
        # print(urlList)
        # for item in urlList:
        #     print(item)
        #     print(item[item.rfind('/')+1:item.rfind('.html')])
        log.info("linkSorted link {}".format(urlList))
        sList = sorted(urlList,key=lambda x: int(x[x.rfind('/')+1:x.rfind('.html')]),reverse=True)
        urlList.clear()
        urlList.extend(sList)

    def linksCallback(self, html, url=None):
        # html.encoding = 'gbk'
        html = html.text
        html = BeautifulSoup(html, "lxml")
        baseUrl = urllib.parse.urlparse(url).scheme + "://" + urllib.parse.urlparse(url).netloc
        # print(baseUrl)
        result = []
        try:
            tags = html.find('div', {'id': 'PageList'}).find_all('a')
            if tags is not None:
                for item in tags:
                    # print(item['href'])
                    tmp = urllib.parse.urljoin(baseUrl,item['href'])
                    if tmp in result or '.html' not in tmp or 'index.html' in tmp:
                        continue
                    result.append(tmp)
        except Exception as e:
            log.error("exception:{}".format(e))
            raise Exception
        # print(result)
        return result

    def scrapeCallback(self, html):
        html.encoding = 'gbk'
        html = html.text
        html = BeautifulSoup(html, "lxml")
        # print(html)
        result = []
        try:
            tags = html.find('div', {'class': 'containerbox boxindex'}).find_all('tr')
            # print(tags)
            if tags is not None:
                for item in tags:
                    ip = item.find_all(text=re.compile("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"))
                    if len(ip) == 0:
                        continue
                    lis = item.find_all('td')
                    liValue = []
                    for li in lis:
                        liValue.append(li.string)
                    # print(liValue)
                    result.append({liValue[0] + ":" + liValue[1]: liValue})
        except Exception as e:
            log.error("exception:{}".format(e))
            raise Exception
        return result

if __name__ == '__main__':
    m = CrawlerProxy66ip()
    m.start()

    for item in m.iteritem(1):
        print(item)
        # m.stop()