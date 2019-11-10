
from flask import current_app,g
from flask.cli import with_appcontext

from database import get_db

def get_flask_db():
    if 'db' not in g:
        g.db=get_db()
        
    return g.db

def close_flask_db(e=None):
    db=g.pop('db',None)
    if db is not None:
        db.close()
