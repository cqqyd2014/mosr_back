


from flask import Blueprint

root_bp = Blueprint('root', __name__, url_prefix='/root')
serverfrom . import restfulapi