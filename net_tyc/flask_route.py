import functools
from flask import Response

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_flask_db

bp = Blueprint('net_tyc', __name__, url_prefix='/net_tyc')

@bp.route('/hello', methods=('GET', 'POST'))
def hello():
    return 'Hello, World!'

@bp.route('/large.csv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')

def iter_all_rows():
    pass

