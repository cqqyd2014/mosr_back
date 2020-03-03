import functools
from flask import Response

from data_manage.restfulapi import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from server.db import get_flask_db

data_manage = Blueprint('data_manage', __name__, url_prefix='/data_manage')

@data_manage.route('/hello', methods=('GET', 'POST'))
def hello():
    return 'Hello, World!'

@data_manage.route('/large.csv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')

def iter_all_rows():
    pass
#outer_trade_detail_view = BankOuterTradeDetailAPI.as_view('system_wait_for_search_company_api')
#bank.add_url_rule('/outer_trade_details/', view_func=BankOuterTradeDetailAPI.as_view('outer_trade_details'))
#system.add_url_rule('/system_parameters/', view_func=SystemParametersAPI.as_view('system_parameters'))
#system.add_url_rule('/system_parameters/<string:s_param>', view_func=SystemParametersAPI.as_view('system_parameters_s_param'))
#system.add_url_rule('/users/', view_func=UsersAPI.as_view('users'))
#system.add_url_rule('/users/<string:u_uuid>', view_func=UsersAPI.as_view('users_uuid'))
#system.add_url_rule('/users/login/<string:login_u_user_name>/<string:login_u_user_password>', view_func=UsersAPI.as_view('users_login'))
#system.add_url_rule('/users/permission/<string:user_uuid_for_permission>', view_func=UsersAPI.as_view('users_permission'))
data_manage.add_url_rule('/database_links/', view_func=DatabaseLinksAPI.as_view('database_links'),methods=['GET'])
data_manage.add_url_rule('/database_links/<string:d_uuid>', view_func=DatabaseLinksAPI.as_view('database_links_pk'),methods=['GET'])
data_manage.add_url_rule('/database_links/check_db_link/<string:check_type>/<string:check_ip>/<string:check_db_port>/<string:check_db_name>/<string:check_db_username>/<string:check_db_password>', view_func=DatabaseLinksAPI.as_view('database_links_check'))
data_manage.add_url_rule('/database_links/', view_func=DatabaseLinksAPI.as_view('database_links_save'),methods=['POST'])
data_manage.add_url_rule('/database_links/', view_func=DatabaseLinksAPI.as_view('database_links_update'),methods=['PUT'])
