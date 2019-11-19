
import datetime
import json
from collections import Iterable
import base64

from urllib import parse

from functools import wraps
from flask import Flask, request
from flask import jsonify
from database.orm import Base

class Base_par:
    '''
    参数的基本类型，需要具体实现
    '''
    def __init__(self):
        pass


#str_p = '2019-01-30 15:29:08.000000'

class DateTime_par(Base_par):
    @staticmethod
    def in_format(value):
        try:
            dateTime_p = datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S.%f')
            return dateTime_p
        except ValueError as e:
            raise RestException('数据不是2019-01-30 15:29:08.000000这样的日期时间型')
    @staticmethod
    def out_format(value):
        return value.strftime('%Y-%m-%d %H:%M:%S.%f')


class Boolen_par(Base_par):
    @staticmethod
    def in_format(value):
        if value in ('True','true','1',1):
            return True
        elif value in ('False','false','0',0):
            return False
        else:
            raise RestException('类型不是布尔')
    @staticmethod
    def out_format(value):
        return value



class Float_par(Base_par):
  
    @staticmethod
    def in_format(value):
        if isinstance(value,string):
            try:
                return float(value)
            except ValueError as identifier:
                RestException('类型不是浮点数')
        if isinstance (value,int):
            value=float(value)
        if isinstance (value,float):
            return value


    @staticmethod
    def out_format(value):
        return value

class Integer_par(Base_par):
    @staticmethod
    def in_format(value):
        if isinstance(value,string):
            try:
                return int(value)
            except ValueError as identifier:
                RestException('类型不是整数')
        if isinstance (value,int):
            return value
        
        
    @staticmethod
    def out_format(value):
        return value

class String_par(Base_par):
    @staticmethod
    def in_format(value):
        return str(value)
    @staticmethod   
    def out_format(value):
        return value


class RestException(Exception):
    def __init__(self,message):
        self.message=message

class RequestParse():
    def __init__(self):
        #定义输入模式
        self.args={}
        #存储输入的数据
        self.in_keys=[]
        #self.out_args={}

    #根据需要生成属性
    def __getattr__(self,name):
        value=self.in_args[name]
        setattr(self,name,value)
        return value
    
    #type类型为这个文件中的类型类，location为form
    def add_argument(self,arg_name,_type,location,required,help,pk=False):
        self.args[arg_name]={'type':_type,'location':location,'required':required,'help':help,'pk':pk}

    #初始化get查询参数，并验证。不关注是否必须项目，只检测名称和类型
    #user = session.query(User).filter(User.id=='5').one()
    def bind_get_request(self,req):
        _dict_query_par=eval(decode64uri(req.args.get("query_string")))
        print("ok")
        print(_dict_query_par)
        _filters=_dict_query_par['filters']
        flag=0
        for _filter in _filters:
            flag+=1
            #检测是否是存在的字段
            if _filter['field'] in self.args.keys():
                #对于存在的类型
                pass
            else:
                raise RestException('索引号：'+str(flag)+';数据:'+str(_dict_query_par)+';字段:'+str(key)+'不是可查询字段')



    #初始化参数验证，并校验。需要关注，是否必选、名称和类型
    def bind_post_request(self, req):
        self.req=req
        args=self.args
        self.in_keys=[]

        datas = json.loads(request.get_data(as_text=True))
        
        #数据格式是{'array_datas:[{},{}]}
        def generate():
            row_flag=0
            for data in datas['array_datas']:
                row_flag+=1
                in_arg={}
                in_key={}
                for key in args:

                    try:
                        key_data=args[key]['type'].in_format(data[key])
                        in_arg[key] =key_data
                        #如果是主键，记录下来
                        if args[key]['pk']:
                            in_key[key]=key_data
                    except RestException as e:
                        raise RestException('索引号：'+str(row_flag)+';数据:'+str(data)+';问题描述：'+key+':'+e.message)
                    except KeyError:
                        if args[key]['required']:
                            raise RestException('索引号：'+str(row_flag)+';数据:'+str(data)+';问题描述：'+args[key]['help'])
                        else:
                            in_arg[key] = None
                self.in_keys.append(in_key)
                yield in_arg
            

        return generate()
        
#把记录根据规范变为字典
def record_json(record,out_fields):
    record_dict=record.__dict__
    result={}
    #print(str(record_dict))
    for key in record_dict:
        if key!='_sa_instance_state':
            value=record_dict[key]
            if key=='last_modified':
                value=DateTime_par.out_format(value)
                result[key]=value
            elif key=='e_tag':
                value=String_par.out_format(value)
                result[key]=value
            else:
                _type=out_fields[key]
                value=_type.out_format(value)
                result[key]=value
    return result



def out_args(*dargs, **dkargs):
    def wrapper(func):
        def _wrapper(*args, **kargs):
            #print ("装饰器参数:", dargs, dkargs)
            #print ("函数参数:", args, kargs)
            #print(dkargs['out_fields'])

            value=func(*args, **kargs)

            #返回元组一般是出现错误，或者返回处理是否成功
            if isinstance(value,tuple):
                return value
            #返回多条记录
            if isinstance(value,Iterable):
                result_list=[]
                for item in value:
                    result_list.append(record_json(item,dkargs['out_fields']))
                return jsonify(result_list),200
            #返回一条记录
            if value.__class__.__bases__[0]==Base:
                #单一记录为了修改，需要返回last_modified和etag
                _dict=value.__dict__
                last_modified=_dict['last_modified']
                e_tag=_dict['e_tag']
                
                return record_json(value,dkargs['out_fields']),200,{'Last-Modified':last_modified,'E-tag':e_tag}

        return _wrapper
    return wrapper

#将主键转换为json


def encode64uri(_str):
    return str(encode64(parse.quote(_str)),encoding="utf-8")


def decode64uri(_str):
    return parse.unquote(decode64(_str))

def decode64(_str):
    return str(base64.b64decode(_str), "utf-8")

def encode64(_str):
    return base64.b64encode(_str.encode("utf-8"))