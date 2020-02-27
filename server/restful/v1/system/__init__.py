
from flask import Blueprint

vesrion = Blueprint('root', __name__)

from . import version