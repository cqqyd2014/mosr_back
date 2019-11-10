import uuid
import datetime

from flask.views import MethodView
from flask import jsonify

from flaskr import db
from net_tyc.database.orm import *
from restful_tools import *


out_fields = {
    'company_name': String_par,
    
}


requestParse=RequestParse()
requestParse.add_argument(arg_name='company_name',_type=String_par,location='form',required=True,help='单位名称是必须的')

class SystemWaitForSearchCompanyAPI(MethodView):
   
    def get(self):
        
        gets=db.get_flask_db().query(NetTycSystemWaitForSearchCompany).all()
        return 'ok'
        
    @out_args(out_fields=out_fields)
    def post(self):
        try:
            requestParse.bind_request(request)
            u_uuid=uuid.uuid1()
            netTycSystemWaitForSearchCompany=NetTycSystemWaitForSearchCompany(u_uuid=u_uuid,u_create_datetime=datetime.datetime.now(),u_company_name=requestParse.company_name,u_start_search_datetime=None,u_end_search_datetime=None,u_status='等待查询')
            db_session=db.get_flask_db()
            db_session.add(netTycSystemWaitForSearchCompany)
            db_session.commit()

            return {'object':netTycSystemWaitForSearchCompany,'code':201}
        except RestException as e:
            return jsonify({'return_status':'error','err_message':e.message})
        

