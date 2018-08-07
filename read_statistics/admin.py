from django.contrib import admin
from .models import ReadNum, ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    """ReadNum模型的后台显示设置"""
    list_display = ('read_num', 'content_object')

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    """ReadDetail模型的后台显示设置"""
    list_display = ('date','read_num', 'content_object')