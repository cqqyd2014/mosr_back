import functools
from flask import Response
from flask_socketio import SocketIO,emit

from bank.restfulapi import BankOuterTradeDetailAPI,BankInfoAPI

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_flask_db

system_socket = Blueprint('system_socket', __name__, url_prefix='/system_socket')

@system_socket.route('/hello', methods=('GET', 'POST'))
def hello():
    return 'Hello, World!'

@system_socket.route('/large.csv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')

def iter_all_rows():
    pass
#outer_trade_detail_view = BankOuterTradeDetailAPI.as_view('system_wait_for_search_company_api')
#bank.add_url_rule('/outer_trade_details/', view_func=BankOuterTradeDetailAPI.as_view('outer_trade_details'))
#bank.add_url_rule('/infos/', view_func=BankInfoAPI.as_view('infos'))

def connect_event(data):
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    sid = request.sid
    print('Client connected'+sid)

