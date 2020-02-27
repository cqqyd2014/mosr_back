'''
Created on 2019年12月1日

@author: xywl2019
'''

import uuid




#session初始化令牌
def get_token(session):
    if session['token']==None:
        session['token']=str(uuid.uuid1())
        #restful_tokens用于存储条件保存的令牌，存在于数组的令牌才能通过验证，通过验证后，令牌失效。
        session['restful_tokens']=[]
    else:
        return session['token']
    
    

