#coding = utf8
"""
-------------------------------------------------
   File Name：     RunParam.py
   Description :  程序运行参数
   Author :       lf
   date：         2018/08/15
-------------------------------------------------
   Change Activity:
                   2018/08/15:  自定义ConfigParse类由UtilTool模块提出，原因是移植方便
-------------------------------------------------
"""
"""
程序运行参数
"""

__author__ = 'lf'

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Util.UtilTool import LazyProperty

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

class RunParam(object):
    """
    系统运行参数类

    """
    def __init__(self):
        self.m_FileParse =  ConfigParse()
        self.m_FileParse.readInit()

    ######################DB CONFIG############################
    @LazyProperty
    def dbType(self):
        return self.m_FileParse.get('DB','type')

    @LazyProperty
    def dbUsrName(self):
        return self.m_FileParse.get('DB','usrname')

    @LazyProperty
    def dbRawName(self):
        return self.m_FileParse.get('DB','rawname')

    @LazyProperty
    def dbChkName(self):
        return self.m_FileParse.get('DB','chkname')

    @LazyProperty
    def dbHost(self):
        return self.m_FileParse.get('DB', 'host')

    @LazyProperty
    def dbPort(self):
        return self.m_FileParse.get('DB', 'port')

    ######################ProxyGetter############################
    @LazyProperty
    def proxyGetterOptions(self):
        return self.m_FileParse.options('ProxyGetter')

    @LazyProperty
    def proxyGetterDict(self):
        return self.m_FileParse.items('ProxyGetter')

    ######################Proxy############################
    @LazyProperty
    def proxyMode(self):
        return self.m_FileParse.get('Proxy','mode')

    @LazyProperty
    def proxyPage(self):
        return self.m_FileParse.get('Proxy','page')

    ######################server API############################
    @LazyProperty
    def serverHostIp(self):
        return self.m_FileParse.get('HOST','IP')

    def serverHostPort(self):
        return self.m_FileParse.get('HOST','PORT')


    ######################LOT CON############################
    @LazyProperty
    def logBasePath(self):
        return self.m_FileParse.get('LOG', 'BasePath')

    @LazyProperty
    def logFileName(self):
        return self.m_FileParse.get('LOG', 'File')

if __name__ == '__main__':
    m = RunParam()
    # print(os.path.realpath(__file__))
    # print(os.path.split(os.path.realpath(__file__)))
    # pwd = os.path.split(os.path.realpath(__file__))[0]
    # print(os.path.split(pwd))
    # print(m.m_FileParse.configPath)
    print(m.dbType)
    print(m.proxyGetterOptions)