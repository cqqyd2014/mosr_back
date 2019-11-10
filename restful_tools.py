
import datetime
import json
from collections import Iterable
import base64

from functools import wraps
from flask import Flask, request
from flask import jsonify


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
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')


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
        if isinstance (value,int):
            value=float(value)
        if isinstance (value,float):
            return value
        else:
            raise RestException('类型不是浮点数')

    @staticmethod
    def out_format(value):
        return value

class Integer_par(Base_par):
    @staticmethod
    def in_format(value):
        if isinstance (value,int):
            return value
        else:
            raise RestException('类型不是整数')
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
        self.in_args=[]
        #self.out_args={}

    #根据需要生成属性
    def __getattr__(self,name):
        value=self.in_args[name]
        setattr(self,name,value)
        return value
    
    #type类型为这个文件中的类型类，location为form
    def add_argument(self,arg_name,_type,location,required,help):
        self.args[arg_name]={'type':_type,'location':location,'required':required,'help':help}

    #初始化参数验证，并校验
    def bind_request(self, req):
        self.req=req
        args=self.args
        datas = json.loads(request.get_data(as_text=True))
        row_flag=0

        for data in datas['arry_datas']:
            row_flag+=1
            in_arg={}
            for key in args:

                try:
                    key_data=args[key]['type'].in_format(data[key])
                    in_arg[key]=key_data
                except RestException as e:
                    raise RestException('索引号：'+str(row_flag)+';数据:'+str(data)+';问题描述：'+key+':'+e.message)
                except KeyError:
                    if args[key]['required']:
                        raise RestException('索引号：'+str(row_flag)+';数据:'+str(data)+';问题描述：'+args[key]['help'])
                    else:
                        in_arg[key]=None

            

            self.in_args.append(in_arg)
        

def record_json(record,out_fields):
    record_dict=record.__dict__
    result={}
    #print(str(record_dict))
    for key in record_dict:
        if key!='_sa_instance_state':
            value=record_dict[key]
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
            if isinstance(value,Iterable):
                result_list=[]
                for item in value:
                    result_list.append(record_json(item,dkargs['out_fields']))
                return jsonify(result_list),200
            else:
                record_json(value,dkargs['out_fields'])

        return _wrapper
    return wrapper




def decode64(_str):
    return str(base64.b64decode(_str), "utf-8")

def encode64(_str):
    return base64.b64encode(_str.encode("utf-8"))