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
    'd_alias':String_par
    
    
    
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
    def get(self,d_uuid=None,check_type=None,check_ip=None,check_db_port=None,check_db_name=None,check_db_username=None,check_db_password=None,save_type=None,save_ip=None,save_db_port=None,save_db_name=None,save_db_username=None,save_db_password=None,save_last_modified=None,save_e_tag=None,save_username=None,save_alias=None,save_memo=None,save_db_uuid=None):
        db_session=db.get_flask_db()
        
        if  d_uuid==None and check_type==None and save_type==None:
            #查询所有记录
            gets=[]
            gets=db_session.query(DatabaseLink).order_by(DatabaseLink.d_add_datetime).all()
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
        elif save_type!=None:
            databaseLink=DatabaseLink()
            return jsonify('ok'),200
                
            
            
    
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
    
    def put(self):
        try:
            db_session=db.get_flask_db()
            #requestParse.bind_post_request(request)
            print('put')

               
            update_datas=requestParse.bind_post_request(request)
            print('okokok1')
            req_datas = json.loads(request.get_data(as_text=True))
            print('okokok2')
            pks=req_datas['_for_xywl2019_update']['pk']
            print(pks)
            print(len(pks))
            for data in update_datas:
                print(data)
                print(data['last_modified'])
                print(data['e_tag'])
                _query=db_session.query(DatabaseLink)
                pks_string=[]
                for pk in pks:
                    
                    _query=_query.filter(getattr(DatabaseLink, pk)==data[pk])
                    pks_string.append({getattr(DatabaseLink, pk):data[pk]})
                print('pkok')
                _query=_query.filter(DatabaseLink.last_modified==data['last_modified'])
                _query=_query.filter(DatabaseLink.e_tag==data['e_tag'])
                get_object=_query.one_or_none()
                print('00000')
                print(get_object)
                print(pks_string)
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

