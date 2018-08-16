#coding = utf8

'''
-------------------------------------------------
   File Name：     SpiderApi.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
---------20180813 修改增加LoadUserAgents 及user_agents.txt 增加更多的User-Agent值
'''

import requests
from requests.models import  Response
import random
import time
import os


def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas

pwd = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(os.path.split(pwd)[0], 'user_agents.txt')
gUasList = LoadUserAgents(configPath)

def requestWeb(url, encode=None, header=None,retryCnt=5, timeout=30, retryFlagList=list(), retryInterval=5,*args,**kwargs):
    """

    :param url:
    :param header:
    :param retryCnt:
    :param timeout:
    :param retry_flag:
    :param retryInterval:
    :param args:
    :param kwargs:
    :return:
    """

    # ua_list = [
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
    #     'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    #     'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    #     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    # ]

    headers= {'User-Agent': random.choice(gUasList),
     'Accept': '*/*',
     'Connection': 'keep-alive',
     'Accept-Language': 'zh-CN,zh;q=0.8'}

    if header and isinstance(header,dict):
        headers.update(header)

    while True:
        try:
            #r.text 返回headers中的编码解析的结果，可以通过r.encoding = 'gbk'来变更解码方式
            #r.content返回二进制结果
            #r.json()返回JSON格式，可能抛出异常
            #r.status_code
            #r.raw返回原始socket respons，需要加参数stream=True
            html = requests.get(url,headers=headers,timeout=timeout, **kwargs)
            if any(f in html.content for f in retryFlagList):
                raise Exception
            if encode :
                html.encoding = encode
            # print(type(html))
            return html
        except Exception as e:
            retryCnt -= 1
            if retryCnt <= 0:
                resp = Response()
                resp.status_code = 200
                return resp
            time.sleep(retryInterval)

def web(url, encode=None,**kwargs):
    """
    WebRequest与lxml获取url对应网页结构
    :param url:
    :param kwargs:
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }

    return requestWeb(url, encode, header)
