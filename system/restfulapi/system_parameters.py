import uuid
import datetime
import json

from flask.views import MethodView
from flask import jsonify
from urllib import parse

from server import db
from orm import *
from restful_tools import *


out_fields = {
    's_param': String_par,
    's_value':String_par,
    's_desc':String_par,
    
    
}



requestParse=RequestParse()
requestParse.add_argument(arg_name='s_param',_type=String_par,location='form',required=True,help='系统参数编码是必须的',pk=True)
requestParse.add_argument(arg_name='s_value',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='s_desc',_type=String_par,location='form',required=False,help=None)


class SystemParametersAPI(MethodView):
   
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
    def get(self,s_param=None):

        if s_param==None:
            #查询所有记录
            gets=[]
            if  'query_string' in request.args:
                try:
                    requestParse.bind_get_request(request)
                except RestException as e:
                    return jsonify({'return_status':'error','err_message':e.message}),500
            else:
                gets=db.get_flask_db().query(SystemParameters).all()
            return gets
        else:
            s_param=json.loads(decode64uri(s_param))['s_param']

            
            get_object=db.get_flask_db().query(SystemParameters).filter(SystemParameters.s_param==s_param).one_or_none()
            return get_object
    
    #新建记录
    def post(self):
        try:
            db_session=db.get_flask_db()
            #requestParse.bind_post_request(request)


               
            db_session.bulk_insert_mappings(SystemParameters,requestParse.bind_post_request(request))
            db_session.commit()
            if (len(requestParse.in_keys))==1:
                pk_str=str(json.dumps(requestParse.in_keys[0]))
                
                encode_pk=encode64uri(pk_str)
                
                return jsonify({'return_status':'ok','num':len(requestParse.in_keys),'links':{'self_herf':request.url+encode_pk}}),201
            #多条记录返回新建数量
            else:
                #编码为网络传输
                for index  in range(len(requestParse.in_keys)):
                    requestParse.in_keys[index]=encode64uri(str(requestParse.in_keys[index]))
                return jsonify({'return_status':'ok','num':len(requestParse.in_keys),'links':{'url_template':request.url,'pks':requestParse.in_keys}}),201
        except RestException as e:
            return jsonify({'return_status':'error','err_message':e.message}),500
        except Exception as e:
            return jsonify({'return_status':'error','err_message':str(e)}),500
        

