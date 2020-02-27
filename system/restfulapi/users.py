'''
Created on 2020年2月23日

@author: xywl2019
用户资源restfulapi
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

out_fields = {
    'u_uuid': String_par,
    'u_user_name':String_par,
    'u_uuid':String_par,
    'u_user_password':String_par,
    'u_nickname':String_par,
    'u_memo':String_par,
    'u_effective':Boolen_par,
    'u_last_login_datetime':DateTime_par
    
    
    
}



requestParse=RequestParse()
requestParse.add_argument(arg_name='u_user_password',_type=String_par,location='form',required=True,help='系统参数编码是必须的',pk=True)
requestParse.add_argument(arg_name='u_user_name',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='u_uuid',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='u_memo',_type=String_par,location='form',required=False,help=None)



class UsersAPI(MethodView):
   
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
    def get(self,u_uuid=None,login_u_user_password=None,login_u_user_name=None,user_uuid_for_permission=None):
        db_session=db.get_flask_db()
        
        if u_uuid==None and login_u_user_password==None and login_u_user_name==None and user_uuid_for_permission==None:
            #查询所有记录
            gets=[]
            gets=db_session.query(Users).all()
            return gets
        elif u_uuid!=None:
            #查询主键
            get_object=db_session.query(Users).filter(Users.u_uuid==u_uuid).one_or_none()
            return get_object
        elif login_u_user_password!=None and login_u_user_name!=None:
            #验证登陆
            
            rs_object=db_session.query(Users).filter(and_(Users.u_user_name==login_u_user_name , Users.u_user_password==login_u_user_password, Users.u_effective==True)).one_or_none()
            if rs_object==None:
                return jsonify({'mosr_message':'用户验证出错，请检查你的输入是否有误'}),404
            else:
                #成功登陆
                rs_object.u_last_login_datetime=datetime.datetime.now()
                return_object=copy.deepcopy(rs_object)
                db_session.commit()
                return return_object
        elif user_uuid_for_permission!=None:
            #查询权限，返回元组结果，先查一级，再查二级，以json返回
            
            m1s=db_session.query(Modules,RolesPermission,UsersToRoles).filter(and_(Modules.m_uuid == RolesPermission.r_module_uuid,RolesPermission.r_role_uuid==Roles.r_uuid,Modules.m_level==1,UsersToRoles.u_uuid==user_uuid_for_permission) ).order_by(Modules.m_order).all()
            menus=[]
            for m1,rp1,utr1 in m1s:
                module={'m_uuid':m1.m_uuid,'m_name':m1.m_name,'m_route_url':m1.m_route_url,'m_type':m1.m_type,'m_icon':m1.m_icon}
                if (m1.m_type=='sub_module'):
                    m2s=db_session.query(Modules,RolesPermission,UsersToRoles).filter(and_(Modules.m_uuid == RolesPermission.r_module_uuid,RolesPermission.r_role_uuid==Roles.r_uuid,Modules.m_up_uuid==m1.m_uuid,UsersToRoles.u_uuid==user_uuid_for_permission) ).order_by(Modules.m_order).all()
                    sub_modules=[]
                    for m2,rp2,utr2 in m2s:
                        sub_module={'m_uuid':m2.m_uuid,'m_name':m2.m_name,'m_route_url':m2.m_route_url,'m_type':m2.m_type,'m_icon':m2.m_icon}
                        sub_modules.append(sub_module)
                    module['sub_module']=sub_modules
                menus.append(module)
                
            
            return jsonify(menus),200
                
            
            
    
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
        

