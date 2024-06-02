from django.urls import path, re_path
from cartapp import views
urlpatterns =[
    path('',views.CartView),
    path('queryAll/',views.queryAll),  # 购物车展示


]