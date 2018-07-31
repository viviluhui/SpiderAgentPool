#coding = utf8

'''
-------------------------------------------------
   File Name：     ProxyApi.py
   Description :
   Author :       lf
   date：         2018/07/18
-------------------------------------------------
   Change Activity:
                  2016/07/18:
-------------------------------------------------
'''

__author__ = 'lf'
import sys
from flask import Flask,jsonify,Response

sys.path.append('../')

#加载其它模块
#import ****

DEBUG = True

app = Flask(__name__)

class JsonResponse(Response):
    @classmethod
    def force_type(cls,response,environ=None):
        # 返回类型是字典或者列表 强制转换成json格式
        if isinstance(response,(dict,list)):
            response = jsonify(response)

        return super(JsonResponse,cls).force_type(response,environ)

app.response_class = JsonResponse


#接口API以json格式返回数据
@app.route('/')
def index():
    '''返回接口帮助文档'''
    return 'hello world'

@app.route('/api/get/')
def get():
    '''返回代理ip'''
    if DEBUG:
        return 'get'
    pass

@app.route('/api/getAll/')
def getAll():
    '''返回所有代理IP'''
    if DEBUG:
        return 'getAll'
    pass

@app.route('/api/delete/')
def delete():
    '''删除指定代理ip'''
    if DEBUG:
        return 'delete'
    pass

@app.route('/api/getStatus/')
def getStatus():
    '''返回服务状态'''
    if DEBUG:
        return 'getStatus'
    pass


def run():
    ip = '127.0.0.1'
    port = 8081
    app.run(ip,port)

if __name__ == '__main__':
    run()