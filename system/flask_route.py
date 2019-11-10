import functools
from flask import Response

from system.restfulapi import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_flask_db

system = Blueprint('system', __name__, url_prefix='/system')

@system.route('/hello', methods=('GET', 'POST'))
def hello():
    return 'Hello, World!'

@system.route('/large.csv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')

def iter_all_rows():
    pass
#outer_trade_detail_view = BankOuterTradeDetailAPI.as_view('system_wait_for_search_company_api')
#bank.add_url_rule('/outer_trade_details/', view_func=BankOuterTradeDetailAPI.as_view('outer_trade_details'))
system.add_url_rule('/pars/', view_func=SystemParAPI.as_view('pars'))
