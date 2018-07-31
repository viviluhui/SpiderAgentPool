#coding = utf8

'''
-------------------------------------------------
   File Name：    DiskCache.py
   Description :  以文件形式保存数据
   Author :       lf
   date：         2018/07/23
-------------------------------------------------
'''
__author__='lf'

import os
import re
import urllib.parse
import zlib
from datetime import datetime,timedelta
try:
    import cPickle as pickle
except:
    import pickle


class DiskCache:
    def __init__(self,cache_dir='cache',expires=timedelta(days=30),compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path,'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result,timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        path = self.url_to_path(url)
        print("path base:" + os.path.basename(path))
        folder = os.path.dirname(path)
        print("folder:" + folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps((result,datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        print("path:" + path)
        with open(path,'wb') as fp:
            fp.write(data)

    def has_expired(self, timestamp):
        return datetime.utcnow() > timestamp + self.expires

    def url_to_path(self, url):
        componts = urllib.parse.urlsplit(url)
        print(componts)
        path = componts.path
        if not path:
            path = '/index.xml'
        elif path.endswith('/'):
            path += 'index.xml'

        filename = componts.netloc + path + componts.query
        # 替换文件路径中非法字符
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        # 文件路径长度255内
        filename = '/'.join(segment[:100] for segment in filename.split('/'))

        return os.path.join(self.cache_dir, filename)