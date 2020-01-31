# -*- coding: UTF-8 -*- 

import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
import time

from docx import Document

from win32com import client as wc


from flaskr import db

def init_app(app):
    app.teardown_appcontext(db.close_flask_db)
    app.cli.add_command(read_attach_command)


@click.command('read-attach')
@with_appcontext
def read_attach_command():
    print("start")
    print("end")




@click.command('solar-charging')
@with_appcontext
def solar_charging_command():
    print("一言不合就充电")
    print("太阳能充电开始")
    while True:
        print('正在充电……请稍后')
        time.sleep(10)
    print('智商检测完毕')



def open_file(file_path):
    #分析文件名后缀,看是什么类型
    if file_path.endswith('.doc'):
        open_doc(file_path)
    if file_path.endswith('.docx'):
        open_docx(file_path)
    if file_path.endswith('.pdf'):
        pass


def open_doc(file_path):
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(file_path)        # 目标路径下的文件
    doc.SaveAs(file_path+'x', 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件    
    doc.Close()
    word.Quit()
    open_docx(file_path+'x')
    os.remove(file_path+'x')




def open_docx(file_path):
    document = Document('demo.docx')  #打开文件demo.docx
    for paragraph in document.paragraphs:
        print(paragraph.text)  #打印各段落内容文本
