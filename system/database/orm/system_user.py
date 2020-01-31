'''
Created on 2019年12月2日

@author: xywl2019
'''

import uuid,datetime

from database.orm import Base,Column,String,Integer,DateTime,Boolean


class SystemUser(Base):
    __tablename__ = "system_user"
    user_uuid = Column(String(37), primary_key=True)
    user_name = Column(String(128),unique=True)
    user_desc_name = Column(String(128))
    user_password = Column(String(128))
    user_password_md5 = Column(String(128))
    user_create_datetime=Column(DateTime,default=datetime.datetime.now)
    user_deleted=Column(Boolean)
    user_delete_datetime=(DateTime)
    user_in_use=Column(Boolean)
    
    last_login_datetime=Column(DateTime)
    last_modified=Column(DateTime,default=datetime.datetime.now)
    e_tag=Column(String(36),default=str(uuid.uuid1()))

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemUser).delete()

    @staticmethod
    def check_user_and_password(db_session,user_name,user_password):
        db_data=db_session.query(SystemUser).filter(SystemUser.user_name==user_name,SystemUser.user_password==user_password).one_or_none()
        return db_data
        
    def __repr__(self):
        return self.user_name+"_"+self.user_desc_name

    def to_json(self):
        json_string = {
            'user_uuid': self.user_uuid,
            'user_name': self.user_name,
            'user_desc_name': self.user_desc_name,
            'user_password': self.user_password

        }
        return json_string

    @staticmethod
    def from_json(json_string):
        return SystemUser(par_code=json_string.get('par_code'), par_desc=json_string.get('par_desc'), par_value=json_string.get('par_value'), par_type=json_string.get('par_type'))
