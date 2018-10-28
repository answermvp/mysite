from django.urls import path
from . import views

urlpatterns = [
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'), # 模态框登录    
    path('login/', views.login, name='login'), # 登录
    path('register/', views.register, name='register'), # 注册
    path('logout/', views.logout, name='logout'), # 登出   
    path('user_info/', views.user_info, name='user_info'), # 个人信息
    path('change_nickname/', views.change_nickname, name='change_nickname'), # 修改昵称
    path('bind_email/', views.bind_email, name='bind_email'), # 绑定邮箱
    path('bind_email_code/', views.send_verification_code, name='send_verification_code'), # 发送验证码
    path('change_password/', views.change_password, name='change_password'), # 修改密码
    path('forgot_password/', views.forgot_password, name='forgot_password'), # 忘记密码
]