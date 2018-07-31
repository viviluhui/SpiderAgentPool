#coding = utf8
"""
程序运行参数
"""

__author__ = 'lf'

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Util.UtilTool import LazyProperty
from Util.UtilTool import ConfigParse

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