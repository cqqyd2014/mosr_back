from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify,current_app

from www.root import root

@root.route('/')
def root():
    user_agent=request.headers.get('User_Agent')
    return 'user_agent is %s' %user_agent