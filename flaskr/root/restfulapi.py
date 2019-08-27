from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify,current_app

from . import root_bp

@root_bp.route('/')
def path_root():
    user_agent=request.headers.get('User_Agent')
    return 'user_agent is %s' %user_agent