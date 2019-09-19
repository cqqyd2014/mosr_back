from flask import current_app, g
from flask.cli import with_appcontext

from .orm import *

def get_db():
    
    Session = sessionmaker(bind=engine)
    session = Session()
        

    return session
