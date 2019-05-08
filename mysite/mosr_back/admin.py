from django.contrib import admin

# Register your models here.
from .models import UserInfo,MySocialTemplate,SysPar

admin.site.register(UserInfo)
admin.site.register(MySocialTemplate)
admin.site.register(SysPar)