"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# 总路由
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home, name='home'), # 首页 http://localhost:8000
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')), # 富文本上传图片
    path('blog/', include('blog.urls')), # 设置分支路由 http://localhost:8000/blog 都由blog下的urls来路由
    path('comment/', include('comment.urls')), # 评论分支路由
    path('likes/', include('likes.urls')), # 点赞分支路由
    path('user/', include('user.urls')), # 用户分支路由                  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
