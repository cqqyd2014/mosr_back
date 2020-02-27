import functools
from flask import Response
from flask_socketio import SocketIO,emit


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from server.db import get_flask_db

def connect_event():
    
    sid = request.sid
    print('Client connected'+sid)

def disconnect_event():
    
    sid = request.sid
    print('Client disconnected'+sid)
