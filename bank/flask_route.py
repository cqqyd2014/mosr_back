import functools
from flask import Response

from bank.restfulapi import BankOuterTradeDetailAPI,BankInfoAPI

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_flask_db

bank = Blueprint('bank', __name__, url_prefix='/bank')

@bank.route('/hello', methods=('GET', 'POST'))
def hello():
    return 'Hello, World!'

@bank.route('/large.csv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')

def iter_all_rows():
    pass
#outer_trade_detail_view = BankOuterTradeDetailAPI.as_view('system_wait_for_search_company_api')
bank.add_url_rule('/outer_trade_details/', view_func=BankOuterTradeDetailAPI.as_view('outer_trade_details'))
bank.add_url_rule('/infos/', view_func=BankInfoAPI.as_view('infos'))
