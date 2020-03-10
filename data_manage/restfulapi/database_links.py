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
out_fields = {
    'd_uuid': String_par,
    'd_type':String_par,
    'd_ip':String_par,
    'd_port':String_par,
    'd_db_name':String_par,
    'd_user_name':String_par,
    'd_password':String_par,
    'd_memo':String_par,
    'd_url':String_par,
    'd_add_datetime':DateTime_par,
    'd_add_username':String_par,
    'd_alias':String_par,
    'is_delete':Boolean_par,
    
    
    
}



requestParse=RequestParse()
requestParse.add_argument(arg_name='d_uuid',_type=String_par,location='form',required=True,help='UUID编码是必须的',pk=True)
requestParse.add_argument(arg_name='d_type',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_ip',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_port',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_db_name',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_user_name',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_password',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_memo',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_add_datetime',_type=DateTime_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_add_username',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='last_modified',_type=DateTime_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='e_tag',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_url',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='d_alias',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='is_delete',_type=Boolean_par,location='form',required=False,help=None)


class DatabaseLinksAPI(MethodView):
   
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
    def get(self,get_top_sql_datas_topnum=None,get_top_sql_datas_uuid=None,get_sql_datas_sql=None,get_top_sql_datas_sql=None,get_sql_datas_uuid=None,get_table_d_uuid=None,d_uuid=None,check_type=None,check_ip=None,check_db_port=None,check_db_name=None,check_db_username=None,check_db_password=None,save_type=None,save_ip=None,save_db_port=None,save_db_name=None,save_db_username=None,save_db_password=None,save_last_modified=None,save_e_tag=None,save_username=None,save_alias=None,save_memo=None,save_db_uuid=None):
        db_session=db.get_flask_db()
        
        if  d_uuid==None and get_top_sql_datas_topnum==None and get_sql_datas_sql==None and get_table_d_uuid==None and check_type==None and save_type==None:
            #查询所有记录
            gets=[]
            gets=db_session.query(DatabaseLink).filter(DatabaseLink.is_delete==False).order_by(DatabaseLink.d_add_datetime).all()
            return gets
        elif d_uuid!=None:
            #查询主键
            get_object=db_session.query(DatabaseLink).filter(DatabaseLink.d_uuid==d_uuid).one_or_none()
            
            return get_object
        elif check_type!=None:
            databaseCommon=DatabaseCommon(db_type=urllib.parse.unquote(check_type),db_address=urllib.parse.unquote(check_ip),db_port=urllib.parse.unquote(check_db_port),db_name=urllib.parse.unquote(check_db_name),db_username=urllib.parse.unquote(check_db_username),db_password=urllib.parse.unquote(check_db_password))
            rs=databaseCommon.checkConnection()
            if (rs=='连接成功'):
                return jsonify({'status':True,'message':rs}),200
            else:
                return jsonify({'status':False,'message':rs}),200
        elif get_table_d_uuid!=None:
            #获取表列表，首先得到link再连接过去获取
            get_object=db_session.query(DatabaseLink).filter(DatabaseLink.d_uuid==get_table_d_uuid).one_or_none()
            #print(get_object.d_type)
            databaseCommon=DatabaseCommon(db_type=get_object.d_type,db_address=get_object.d_ip,db_port=get_object.d_port,db_name=get_object.d_db_name,db_username=get_object.d_user_name,db_password=get_object.d_password)
            databaseCommon.getConnection()
            tables=copy.deepcopy(databaseCommon.getTables())
            databaseCommon.closeConnection()
            return jsonify({'tables':tables}),200
        elif get_top_sql_datas_sql!=None and get_top_sql_datas_topnum!=None and get_top_sql_datas_uuid!=None:
            print(get_top_sql_datas_sql)
            print(get_top_sql_datas_uuid)
            get_object=db_session.query(DatabaseLink).filter(DatabaseLink.d_uuid==get_top_sql_datas_uuid).one_or_none()
            rs={}
            databaseCommon=DatabaseCommon(db_type=get_object.d_type,db_address=get_object.d_ip,db_port=get_object.d_port,db_name=get_object.d_db_name,db_username=get_object.d_user_name,db_password=get_object.d_password)
            try:
                databaseCommon.getConnection()
                rs=databaseCommon.getRowCellsBySQLTop(get_top_sql_datas_sql,get_top_sql_datas_topnum)
            finally:
                databaseCommon.closeConnection()
            return jsonify(rs),200
                
            
            
    
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

