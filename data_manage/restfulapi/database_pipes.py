'''
Created on 2020年2月23日

@author: xywl2019
数据联接资源restfulapi
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
from orm.tb_database_pipe import DatabasePipe
out_fields = {
    'p_uuid': String_par,
    'p_data_link_uuid':String_par,
    'p_data_link_alias_name':String_par,
    'p_table_name':String_par,
    'p_source_type':String_par,
    'p_source_sql':String_par,
    'p_add_datetime':DateTime_par,
    'is_delete':Boolean_par,
    'p_name':String_par,
    
}



requestParse=RequestParse()
requestParse.add_argument(arg_name='p_uuid',_type=String_par,location='form',required=True,help='UUID编码是必须的',pk=True)
requestParse.add_argument(arg_name='p_data_link_uuid',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='p_data_link_alias_name',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='p_table_name',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='p_source_type',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='p_source_sql',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='last_modified',_type=DateTime_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='e_tag',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='is_delete',_type=Boolean_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='p_add_datetime',_type=DateTime_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='p_name',_type=String_par,location='form',required=False,help=None)


class DatabasePipesAPI(MethodView):
   
    '''
    #查询所有记录
    @out_args(out_fields=out_fields)
    def get(self):
        gets=[]
        if  'query_string' in request.args:
            try:
                requestParse.bind_get_request(request)
            except RestException as e:
                return jsonify({'return_status':'error','err_message':e.message}),500
        else:
            gets=db.get_flask_db().query(SystemPar).all()
        return gets
    '''
    
    #查询单个记录，通过主键
    @out_args(out_fields=out_fields)
    def get(self,p_uuid=None):
        db_session=db.get_flask_db()
        
        if  p_uuid==None:
            #查询所有记录
            gets=[]
            gets=db_session.query(DatabasePipe).filter(DatabasePipe.is_delete==False).order_by(DatabasePipe.p_add_datetime).all()
            
            return gets
        elif p_uuid!=None:
            #查询主键
            get_object=db_session.query(DatabasePipe).filter(DatabasePipe.p_uuid==p_uuid).one_or_none()
            return get_object
        
                
            
            
    
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

