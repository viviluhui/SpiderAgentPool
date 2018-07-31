#coding = utf8

'''
-------------------------------------------------
   File Name：     SpiderApi.py
   Description :
   Author :       lf
   date：         2018/07/20
-------------------------------------------------
'''
import sys
import re
import os
import urllib.response
import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar

class HttpBrowser:
    # 页面初始化
    def __init__(self):
        self.cookiefile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'cookie')
        self.cookie = http.cookiejar.LWPCookieJar(self.cookiefile)
        self.opener = None

    def cookieHttpBrowser(self,url,num_retries=2):
        #httpCookie = http.cookiejar.MozillaCookieJar()
        #httpCookie = http.cookiejar.LWPCookieJar()
        print(url)
        #self.cookie.load(ignore_discard=True, ignore_expires=True)
        ###设置header
        values = {'username': 'cqc', 'password': 'XXXX'}
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Referer': 'http://www.zhihu.com/articles'}
        data = urllib.parse.urlencode(values)
        #req = urllib.request.Request(url,data,headers)

        req = urllib.request.Request(url)
        handler = urllib.request.HTTPCookieProcessor(self.cookie)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        try:
            #html = opener.open(req).read()
            html = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print('HTTPCODE:', e.code)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.cookieHttpBrowser(url, num_retries - 1)
        except urllib.error.URLError as e:
            print(e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e,'code') and 500 <= e.code < 600:
                    return self.cookieHttpBrowser(url,num_retries-1)
        self.cookie.save(ignore_discard=True, ignore_expires=True)
        return html

    def proxyHttpBrowser(self, url):
        print(url)
        enable_proxy = True
        proxy_handler=urllib.request.ProxyHandler({"http":"http://some-proxy.com:8080"})
        handler = urllib.request.HTTPCookieProcessor(self.cookie)
        if enable_proxy:
            opener = urllib.request.build_opener(proxy_handler)
        else:
            opener = urllib.request.build_opener(handler)
        #安装全局opener urllib.request.urlopen将使用此全局opener
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
            #描述了获取的页面情况描述了获取的页面情况 通常是服务器发送的特定头headers
            print(response.info())
            html = response.read()
        except urllib.error.HTTPError as e:
            print('HTTPCODE:', e.code)
            html=None
        except urllib.error.URLError as e:
            print(e.reason)
            html = None
        self.cookie.save(ignore_discard=True, ignore_expires=True)
        return html


    def httpBrowser(self,url,headers=None,proxy=None ,num_retries=2,data=None):
        print(url)
        ###设置header
        values = {'username': 'cqc', 'password': 'XXXX'}
        #headers = {'User-Agent': user_anget}
        #data = urllib.parse.urlencode(values)
        #req = urllib.request.Request(url,data,headers)
        req = urllib.request.Request(url,data,headers or {})
        code = None
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).schema,proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(req)
            html = response.read()
            code = response.code
        except urllib.error.HTTPError as e:
            print('HTTPCODE:',e.code)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.cookieHttpBrowser(url, num_retries - 1)
        except urllib.error.URLError as e:
            print('URLError:' + e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.httpBrowser(url,headers,proxy,num_retries - 1)
        #httphandler = urllib.request.HTTPHandler(debuglevel=1)
        #httpsHandler = urllib.request.HTTPSHandler(debuglevel=1)
        #opener = urllib.request.build_opener(httphandler,httpsHandler)
        return {'html':html,'code':code}
