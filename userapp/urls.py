from django.urls import path
from userapp import views

urlpatterns = [
    path('register/', views.RegisterView),# 用户注册
    path('center/', views.CenterView),# 用户中心
    path('login/', views.LoginView),# 用户中心
    path('loadCode/', views.loadCode),# 生成验证码
    path('checkcode/', views.CheckCode),# 校验验证码
    path('logout/', views.logout),# 退出登录
    path('address/', views.address),# 地址管理
    path('loadAddr/', views.loadAddr),# 查询区划




]