from django.urls import path, re_path, include
from orderapp import views

urlpatterns = [
    path('',views.order_view),  #
    path('toOrder/',views.toOrder),  #
    path('toPay/',views.toPay),  # 支付功能



]
