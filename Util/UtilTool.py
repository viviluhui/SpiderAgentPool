#coding = utf8


__author__ = 'lf'

import os
import requests
import subprocess

"""
    单实例模式
"""
class Singleton(type):
    def __init__(self, *args,**kwargs):
        self.__instance = None
        super(Singleton,self).__init__(*args,**kwargs)

    def __call__(self,*args,**kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton,self).__call__(*args,**kwargs)
        return self.__instance

"""
    Python内置的@property装饰器就是负责把一个方法变成属性调用的
"""
class LazyProperty(object):
    def __init__(self,func):
        self.func = func

    def __get__(self, instance, owner):
        val = self.func(instance)
        setattr(instance,self.func.__name__,val)
        return val

"""
    封装配置文件解析类
"""
from configparser import ConfigParser   #py3

class ConfigParse(ConfigParser):
    def __init__(self):
        super(ConfigParse, self).__init__()

    def optionxform(self, optionstr):
        return optionstr

    def readInit(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.configPath = os.path.join(os.path.split(self.pwd)[0],'config.ini')
        self.read(self.configPath,'utf8')

def validNetWork():
    # exit_code = os.popen('ping www.baidu.com').read()
    # print(exit_code)
    # if exit_code:
    #     raise Exception('connect failed.')
    ret = subprocess.call('ping -n 2 -w 1 www.baidu.com',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if ret:
        raise Exception('connect failed.')

# noinspection PyPep8Naming
def validUsefulProxy(proxy):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过10秒的代理就不要了
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200:
            # logger.info('%s is ok' % proxy)
            return True
    except Exception as e:
        # logger.error(str(e))
        return False
