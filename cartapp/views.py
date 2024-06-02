from django.shortcuts import render, HttpResponse, redirect
from cartapp.cartmanager import *


# Create your views here.

def CartView(request):
    if request.method == "POST":
        # 这句话的设置是为了保证数据能够实时保存在session中
        request.session.modified = True


        # 获取用户当前操作类型的变量值

        flag = request.POST.get('flag', '')

        # 判断用户当前的操作类型
        if flag == 'add':  # 表示加入购物车
            #  获取cartManager对象

            cartManager = getCartManger(request)
            # 加入购物车操作
            cartManager.add(**request.POST.dict())

        elif flag == "plus":# 表示要增加购物车操作
            # 获取cartManager对象
            # print("我是傻逼")
            cartManager = getCartManger(request)
            # 增加商品数量
            cartManager.update(step=1,**request.POST.dict())  # step=1 <=> +1

        elif flag == "minus": #减少购物车商品
            # 获取cartManager对象
            cartManager = getCartManger(request)
            # 减少购物车商品
            cartManager.update(step=-1, **request.POST.dict())
        elif flag == "delete":  #从购物车中间删除宝贝
            # 获取cartManager对象
            cartManager = getCartManger(request)
            # 删除购物车商品
            cartManager.delete(**request.POST.dict())
        return redirect('/cart/queryAll')






def queryAll(request):
    # 获取getCarManger对象
    cartManager = getCartManger(request)
    # 获取当前登录用户的购物项表中的所有的信息
    cartItemlist = cartManager.queryAll()
    return render(request, 'cart.html', {"cartItemlist": cartItemlist})
