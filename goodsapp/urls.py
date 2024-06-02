from django.urls import re_path,path, include
from goodsapp import views


urlpatterns = [
    path('',views.IndexView),
    path('category/<int:cid>/',views.IndexView),
    path('goodsdetails/<int:gid>/',views.DetailView)


]