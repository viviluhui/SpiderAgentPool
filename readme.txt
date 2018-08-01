
互联网免费代理池
    爬取互联网免费代理，采集数据使用SSDB或其它存储，采用多线程对代理进行验证，对外提供WEB API调用方式。

下载安装
----GIT SHELL方式
git clone git@github.com:viviluhui/SpiderAgentPool.git
----网站zip下载
https://github.com/viviluhui/SpiderAgentPool 下载zip文件

开发环境
windows 10 Python 3.5

依赖关系
Flask           1.0.2
requests        2.19.1
pyssdb          0.4.1
APScheduler     3.5.1
beautifulsoup4  4.6.0


配置文件config.ini
[DB]                数据库配置
[ProxyGetter]       互联网免费代理提供者，键值对应模块Spider类名
[Proxy]             爬虫更新侧略
[HOST]              WEB服务设置
[LOG]               日志设置

启动
    总启动：运行RUN/main.py即可
    依次启动：运行Api/ProxyApi.py,Schedule/ProxyRefreshSchedule.py和Schedule/ProxyValidSchedule.py

使用
    查看数据库或者通过WEB API访问

API


扩展代理
    Spider编写类继承CrawlerProxyBase,按需编写方法linksCallback=None,scrapeCallback=None,linkSorted=None,__init__时传入父类
    linksCallback方法：    抓取网页超链接，返回列表（列表中url为完整url)
    scrapeCallback方法：   抓取网页代理，返回列表，格式如下[{"IP:PORT","任意值"},{"IP:PORT","任意值"}]
    linkSorted方法：       对抓取超链接进行排序，CrawlerProxyBase爬取方式为先进后出
    配置文件ProxyGetter项填加新增类名与抓取初始地址




