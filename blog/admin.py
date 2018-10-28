from django.contrib import admin
from .models import BlogType, Blog # 导入模型

# 这个文件用于将写好的模型添加到后台

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    '''这个类用来定制BlogType模型在后台怎样展示'''
    # 显示模型中的哪些属性
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''这个类用来定制Blog模型在后台怎样展示'''
    list_display = ('id','title','blog_type','author','get_read_num','create_time','last_updated_time')
    