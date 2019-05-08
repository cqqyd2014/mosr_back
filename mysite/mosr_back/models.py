from django.db import models

# Create your models here.


class SysPar(models.Model):
    sys_code=models.CharField(max_length=128,primary_key=True)
    sys_desc=models.CharField(max_length=256)
    sys_value=models.CharField(max_length=256)
    sys_type=models.CharField(max_length=32)#STRING/INT/DATE/DATETIME


class UserInfo(models.Model):
    user_name=models.CharField(max_length=128)
    user_password=models.CharField(max_length=128)
    user_uuid=models.CharField(max_length=32,primary_key=True)
    user_display_name=models.CharField(max_length=32,default='')


class MySocialTemplate(models.Model):
    user_uuid=models.CharField(max_length=32)
    template_uuid=models.CharField(max_length=32)
    template_name=models.CharField(max_length=32)
    template_create_datetime=models.DateTimeField
    class Meta:
         unique_together = ("user_uuid", "template_uuid") #这是重点

