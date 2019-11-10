import uuid
import datetime

from flask.views import MethodView
from flask import jsonify

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
requestParse.add_argument(arg_name='par_code',_type=String_par,location='form',required=True,help='系统参数编码是必须的')
requestParse.add_argument(arg_name='par_desc',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='par_value',_type=String_par,location='form',required=False,help=None)
requestParse.add_argument(arg_name='par_type',_type=String_par,location='form',required=False,help=None)


class SystemParAPI(MethodView):
   


    @out_args(out_fields=out_fields)
    def get(self):
        gets=[]
        if  'query_string' in request.args:
            query_json=name = json.loads(decode64(request.args.get("query_string")))
        else:
            gets=db.get_flask_db().query(SystemPar).all()
        return gets

    
        
    #@out_args(out_fields=out_fields)
    def post(self):
        try:
            db_session=db.get_flask_db()
            requestParse.bind_request(request)
            '''
            for in_arg in requestParse.in_args:
                print(in_arg)
                bankOuterTradeDetail=BankOuterTradeDetail(account_no=in_arg['account_no'],account_name=in_arg['account_name'],card_no=in_arg['card_no'],trade_datetime=in_arg['trade_datetime']
                ,trade_seq=in_arg['trade_seq'],amount=in_arg['amount'],banlance=in_arg['banlance'],trade_code=in_arg['trade_code'],opp_bank_code=in_arg['opp_bank_code']
                ,opp_bank_name=in_arg['opp_bank_name'],opp_account_no=in_arg['opp_account_no'],opp_account_name=in_arg['opp_account_name'],
                memo=in_arg['memo'],bank_code=in_arg['bank_code'])
                
                db_session.add(bankOuterTradeDetail)
            '''
               
            db_session.bulk_insert_mappings(SystemPar,requestParse.in_args)
            db_session.commit()

            return jsonify({'return_status':'ok','num':len(requestParse.in_args)}),201
        except RestException as e:
            return jsonify({'return_status':'error','err_message':e.message}),500
        except Exception as e:
            return jsonify({'return_status':'error','err_message':str(e)}),500
        

