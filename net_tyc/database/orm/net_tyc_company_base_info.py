import json
from python_common.common import DateTimeEncoder
from . import Base,Column,String,Integer,Text,DateTime,Boolean,Date,Numeric



class NetTycCompanyBaseInfo(Base):
    __tablename__ = "net_tyc_company_base_info"
    c_name=Column(String(1024), unique=True)
    c_uscc=Column(String(64), unique=True)#统一社会信用代码
    c_reg_capital=Column(Numeric)
    c_real_capital=Column(Numeric)
    c_start_date=Column(Date)
    c_status=Column(String(64))
    c_tax_code=Column(String(64))
    c_org_code=Column(String(64))
    c_reg_code=Column(String(64))#工商注册号
    c_type=Column(String(64))
    c_industry=Column(String(64))
    c_permit_date=Column(Date)
    c_permit_gov=Column(String(512))
    c_business_period=Column(String(512))
    c_tax_level=Column(String(512))
    c_staff=Column(String(512))
    c_old_name=Column(String(512))
    c_english_name=Column(String(1024))#英文名称
    c_social_security_staff=Column(Integer)#参保人数
    c_addr=Column(String(1024))
    c_business=Column(Text)
    c_company_id=Column(String(64), primary_key=True)
    c_tianyancha_link=Column(String(1024))

    def relSaveOrUpdate(self, session):
        db_data = session.query(CompanyBaseInfo).filter(
            CompanyBaseInfo.c_company_id == self.c_company_id).one_or_none()
        if db_data == None:
            session.add(self)
    
    def mainSaveOrUpdate(self, session):
        db_data = session.query(CompanyBaseInfo).filter(
            CompanyBaseInfo.c_company_id == self.c_company_id).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.c_name=self.c_name
            db_data.c_uscc=self.c_uscc
            db_data.c_reg_capital=self.c_reg_capital
            db_data.c_real_capital=self.c_real_capital
            db_data.c_start_date=self.c_start_date
            db_data.c_status=self.c_status
            db_data.c_tax_code=self.c_tax_code
            db_data.c_org_code=self.c_org_code
            db_data.c_reg_code=self.c_reg_code
            db_data.c_type=self.c_type
            db_data.c_industry=self.c_industry
            db_data.c_permit_date=self.c_permit_date
            db_data.c_permit_gov=self.c_permit_gov
            db_data.c_business_period=self.c_business_period
            db_data.c_tax_level=self.c_tax_level
            db_data.c_staff=self.c_staff
            db_data.c_old_name=self.c_old_name
            db_data.c_english_name=self.c_english_name
            db_data.c_social_security_staff=self.c_social_security_staff
            db_data.c_addr=self.c_addr
            db_data.c_business=self.c_business
            db_data.c_company_id=self.c_company_id
            db_data.c_tianyancha_link=self.c_tianyancha_link



    @staticmethod
    def delete_all(db_session):
        db_session.query(CompanyBaseInfo).all().delete()
        #print("删除成功")


    def __repr__(self):
        return self.c_name+self.c_uscc+'/'+self.c_tianyancha_company_id

    def to_json(self):
        json_string = {
            'c_company_id': self.c_company_id,
            'c_name': self.c_name,
            'c_reg_capital':self.c_reg_capital,
            'c_real_capital':self.c_real_capital,
            'c_tianyancha_link':self.c_tianyancha_link,
            'c_start_date': json.dumps(self.c_start_date, cls=DateTimeEncoder),
            'c_uscc': self.c_uscc,
            'c_status': self.c_status,
            'c_tax_code': self.c_tax_code,
            'c_org_code': self.c_org_code,
            'c_reg_code': self.c_reg_code,
            'c_type': self.c_type,

            

        }
        return json_string