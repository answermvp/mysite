from django.urls import path
from . import views

# 分支路由，由http://localhost:8000/blog/ 开始
urlpatterns = [
    # 博客列表页 http://localhost:8000/blog/
    path('', views.blog_list, name='blog_list'),
    # 博文详情页 http://localhost:8000/blog/‘博文的主键：id’
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    # 同类博文页 http://localhost:8000/blog/type/‘博文类型的主键：id’
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),
    # 按照日期分类
    path('date/<int:year>/<int:month>', views.blogs_with_date, name="blogs_with_date"),
]
