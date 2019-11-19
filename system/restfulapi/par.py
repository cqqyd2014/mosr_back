import uuid
import datetime
import json

from flask.views import MethodView
from flask import jsonify
from urllib import parse

from flaskr import db
from system.database.orm import *
from restful_tools import *


out_fields = {
    'par_code': String_par,
    'par_desc':String_par,
    'par_value':String_par,
    'par_type':Integer_par
    
}



requestParse=RequestParse()
requestParse.add_argument(arg_name='par_code',_type=String_par,location='form',required=True,help='系统参数编码是必须的',pk=True)
requestParse.add_argument(arg_name='par_desc',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='par_value',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='par_type',_type=String_par,location='form',required=False,help=None)


class SystemParAPI(MethodView):
   
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
    def get(self,par_code=None):

        if par_code==None:
            #查询所有记录
            gets=[]
            if  'query_string' in request.args:
                try:
                    requestParse.bind_get_request(request)
                except RestException as e:
                    return jsonify({'return_status':'error','err_message':e.message}),500
            else:
                gets=db.get_flask_db().query(SystemPar).all()
            return gets
        else:
            par_code=json.loads(decode64uri(par_code))['par_code']

            
            get_object=db.get_flask_db().query(SystemPar).filter(SystemPar.par_code==par_code).one_or_none()
            return get_object
    
    #新建记录
    def post(self):
        try:
            db_session=db.get_flask_db()
            #requestParse.bind_post_request(request)


               
            db_session.bulk_insert_mappings(SystemPar,requestParse.bind_post_request(request))
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
        

