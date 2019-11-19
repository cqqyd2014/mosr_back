#encoding=utf-8
import os
from neo4j import GraphDatabase
from database import get_db,ProcessDetail,QueryTemplate,JobQueue,ImportData
import datetime
import uuid
from sqlalchemy import desc
import json
import ast
import csv
import sys
import platform
import os
import locale
import subprocess

from system.database.orm import *


from python_common.database_common import Database
from .opendb_getjob import opendb_getjob




def import_data():
    opendb_getjob('import_data',job)
    
def job(db_session,queue,current):
           
    import_command=queue.u_body
    print(import_command)
    impor_array=import_command.split(' ')
        #r_import_command=
    child1 = subprocess.check_output(impor_array)
        #print(child1.decode('utf-8'))
        
        #print(r_import_command)
    queue.u_back_message=child1.decode('utf-8')
    current=datetime.datetime.now()
            
    return current
    

def main():

    import_data()

if __name__ == '__main__':
  main()