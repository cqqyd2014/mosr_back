'''
Created on 2020年2月23日

@author: xywl2019
Hbase基本信息及管理restfulapi
'''

from common.mosr_message import *
from flask.views import MethodView
from flask import jsonify
from urllib import parse
import copy
from server import db
from orm import *
from restful_tools import *
from sqlalchemy import and_,or_
import urllib



from common.database_common import DatabaseCommon
from _datetime import date
import requests
from data_manage import hbase_ip


def get_hbase_rest(url):
    _header = {'content-type': 'application/json','Accept': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    
    return requests.get("http://"+hbase_ip+":2019/"+url,headers=_header).json()

def get_version():
    return get_hbase_rest("version/cluster")
    
def get_namespaces():

    return get_hbase_rest("namespaces")

def get_status():
    return get_hbase_rest("status/cluster")

def get_all_tables():
    all_tables=get_hbase_rest("")['table']
    for table in all_tables:
        table_schema=get_table_schema(table['name'])
        table_regions=get_table_regions(table['name'])
        table['schema']=table_schema
        table['regions']=table_regions
        
    
    return all_tables

def get_table_schema(table_name):
    return get_hbase_rest(table_name+"/schema")

def get_table_regions(table_name):
    return get_hbase_rest(table_name+"/regions")
out_fields = {
    'd_uuid': String_par,
    
    
}



requestParse=RequestParse()
requestParse.add_argument(arg_name='d_uuid',_type=String_par,location='form',required=True,help='UUID编码是必须的',pk=True)


class HbaseAdminAPI(MethodView):

    #查询单个记录，通过主键
    @out_args(out_fields=out_fields)
    def get(self,param=None,param1=None,param2=None,param3=None):

        #只有方法没有参数
        args = []
        kwargs = {}
        if (param!=None and param1==None):
            try:
                return jsonify(eval(param)()),200
            except NameError as e:
                return "{}",404
        elif (param!=None and param1!=None and param2==None):
            args = [param1]
        elif (param!=None and param1!=None and param2!=None and param3==None):
            args = [param1,param2]
        elif (param!=None and param1!=None and param2!=None and param3!=None):
            args = [param1,param2,param3]
        if args==[]:
            return "{}",200
        else:
            return jsonify(eval(param)(*args, **kwargs)),200
    '''
        if param=='version':
            return jsonify(get_version()),200#{  "Version": "2.2.3"}

        elif param=='status':
            return jsonify(get_status()),200
        elif param=='namespaces':
            return jsonify(get_namespaces()),200
        elif param=='all_tables':
            return jsonify(get_all_tables()),200#{  "table": []}
                    
    '''
            
    
    #新建记录
    def post(self):
        try:
            db_session=db.get_flask_db()
            #requestParse.bind_post_request(request)
            #print('post')

               
            db_session.bulk_insert_mappings(DatabaseLink,requestParse.bind_post_request(request))
            db_session.commit()
            #主键为uuid
            if (len(requestParse.in_keys))==1:
                #pk_str=str(json.dumps(requestParse.in_keys[0]))
                #print(requestParse.in_keys[0])
                #{'d_uuid': 'e642226b-1812-44f3-8311-ad351ec0d6fa'}
                encode_pk=parse.quote(requestParse.in_keys[0]['d_uuid'])
                #print(request.url+encode_pk)
                return jsonify({'status':True,'num':1,'links':{'self_herf':request.url+encode_pk}}),201
            #多条记录返回新建数量
            else:
                #编码为网络传输
                links=[]
                for index  in range(len(requestParse.in_keys)):
                    #requestParse.in_keys[index]=encode64uri(str(requestParse.in_keys[index]))
                    links.append(request.url+parse.quote(requestParse.in_keys[index]['d_uuid']))
                return jsonify({'status':True,'num':len(requestParse.in_keys),'links':links}),201
        except RestException as e:
            return jsonify({'status':False,'message':e.message}),500
        except Exception as e:
            return jsonify({'status':False,'message':str(e)}),500
    
    def delete(self):
        
        try:
            db_session=db.get_flask_db()
            #requestParse.bind_post_request(request)
            
            #update_datas=requestParse.bind_post_request(request)
            req_datas = json.loads(request.get_data(as_text=True))
            
            pks=req_datas['array_pks']
            
            for pk in pks:
                _query=db_session.query(DatabaseLink)
                pks_string=[]
                #{ 'array_pks': [{ 'd_uuid': record.key, 'last_modified': record.last_modified, 'e_tag': record.e_tag }] }
                
                for prop in pk:
                    _query=_query.filter(getattr(DatabaseLink, prop)==pk[prop])
                    pks_string.append({getattr(DatabaseLink, prop):pk[prop]})
                
                get_object=_query.one_or_none()
                if get_object==None:
                    return jsonify({'status':False,'message':'删除的资源不可用或已经不是最新状态'}),404
                #通过验证，开始更新，生成新的e_tag和last_modified
                #db_session.delete(get_object)
                get_object['is_delete']=False
                
            db_session.commit()
            #主键为uuid
            if (len(pks))==1:
                #pk_str=str(json.dumps(requestParse.in_keys[0]))
                #print(requestParse.in_keys[0])
                #{'d_uuid': 'e642226b-1812-44f3-8311-ad351ec0d6fa'}
                
                #print(request.url+encode_pk)
                return jsonify({'status':True,'num':1}),204
            #多条记录返回新建数量
            else:
                #编码为网络传输
                
                return jsonify({'status':True,'num':len(pks)}),204
        except RestException as e:
            print(e)
            return jsonify({'status':False,'message':e.message}),500
        except Exception as e:
            print(e)
            return jsonify({'status':False,'message':str(e)}),500    

    def put(self):
        try:
            db_session=db.get_flask_db()
            #requestParse.bind_post_request(request)
               
            update_datas=requestParse.bind_post_request(request)
            req_datas = json.loads(request.get_data(as_text=True))
            pks=req_datas['_for_xywl2019_update']['pk']
            for data in update_datas:
                _query=db_session.query(DatabaseLink)
                pks_string=[]
                for pk in pks:
                    
                    _query=_query.filter(getattr(DatabaseLink, pk)==data[pk])
                    pks_string.append({getattr(DatabaseLink, pk):data[pk]})
                _query=_query.filter(DatabaseLink.last_modified==data['last_modified'])
                _query=_query.filter(DatabaseLink.e_tag==data['e_tag'])
                get_object=_query.one_or_none()
                if get_object==None:
                    return jsonify({'status':False,'message':'修改的资源不可用或已经不是最新状态'}),404
                #通过验证，开始更新，生成新的e_tag和last_modified
                get_object.e_tag=uuid.uuid1()
                get_object.last_modified=datetime.datetime.now()
                for key in data:
                    if key not in ['e_tag','last_modified']:
                        setattr(get_object, key, data[key])
                
            db_session.commit()
            #主键为uuid
            if (len(requestParse.in_keys))==1:
                #pk_str=str(json.dumps(requestParse.in_keys[0]))
                #print(requestParse.in_keys[0])
                #{'d_uuid': 'e642226b-1812-44f3-8311-ad351ec0d6fa'}
                encode_pk=parse.quote(requestParse.in_keys[0]['d_uuid'])
                #print(request.url+encode_pk)
                return jsonify({'status':True,'num':1,'links':{'self_herf':request.url+encode_pk}}),201
            #多条记录返回新建数量
            else:
                #编码为网络传输
                links=[]
                for index  in range(len(requestParse.in_keys)):
                    #requestParse.in_keys[index]=encode64uri(str(requestParse.in_keys[index]))
                    links.append(request.url+parse.quote(requestParse.in_keys[index]['d_uuid']))
                return jsonify({'status':True,'num':len(requestParse.in_keys),'links':links}),201
        except RestException as e:
            print(e)
            return jsonify({'status':False,'message':e.message}),500
        except Exception as e:
            print(e)
            return jsonify({'status':False,'message':str(e)}),500    

