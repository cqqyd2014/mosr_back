import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
from neo4j import GraphDatabase

import datetime
import uuid
import time
from .download_data import download_data
from .import_data import import_data
from .clean_neo4j import clean_neo4j
from .neo4j_command import neo4j_command
from .algoUnionFind import unionFind

import sys


from system.database.orm import *
from flaskr import db


def init_app(app):
    app.teardown_appcontext(db.close_flask_db)
    app.cli.add_command(main_run_command)


@click.command('back-queue')
@with_appcontext
def main_run_command():


    ps=0
    try:
        db_session=db.get_flask_db()
        #读取执行的间隔
        polling_second=db_session.query(SystemPar).filter(SystemPar.par_code=='polling_second').one()
        ps=int(polling_second.par_value)
        db_session.commit()
        
    except:
        db_session.rollback()
        raise
    finally:
        pass
    print("连接数据库成功，轮询间隔"+str(ps))
    if ps>0:
        while True:
            
            #
            download_data()
            import_data()
            clean_neo4j()
            neo4j_command()
            unionFind()
            time.sleep(ps)
