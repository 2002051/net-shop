import jsonpickle
from django.shortcuts import render,redirect,HttpResponse


# Create your views here.
from orderapp import models
from cartapp.cartmanager import getCartManger


def order_view(request):
    # 先判断用户是否已经登录，如果没有登录就先去登录

    # 先获取请求参数cartitems
    cartitems = request.GET.get("cartitems",'')

    # 获取请求参数和当前登录用户信息
    user = request.session.get('user','')

    #判断是否登录
    if not user:# 用户未登录

        return redirect("/user/login/?redirct=order&cartitems="+cartitems)  #传递一个参数，以告诉登录的视图函数，这是由订单页面跳转过去的，做出不一样的处理

    return redirect("/order/toOrder/?cartitems="+cartitems)






def toOrder(request):
    # 接收请求参数
    cartitems = request.GET.get('cartitems','')
    # 将cartitems 进行反序列化 转换成一个列表了,json无论长什么样就算长着字典的样子，类型查看也是一个str，肯定需要反序列化

    cartitemsList = jsonpickle.loads(cartitems)                                  # print(cartitems)#[{"goodsid":"6","sizeid":"14","colorid":"18"}]

    cartitemObjList = [getCartManger(request).get_cartitems(**ci) for ci in cartitemsList if ci  ]

    # 获取用户默认的收件地址
    user = jsonpickle.loads(request.session.get("user"))  #先获取用户信息
    addr = user.address_set.get(isdefault=True)  #获取默认收货地址

    # 支付总金额
    totalPrice = 0
    for cio in cartitemObjList:#遍历购物车里面每一项
        totalPrice += cio.getTotalPrice()


    return render(request,'order.html',{'cartitemsList':cartitemObjList,'addr':addr,'totalPrice':totalPrice})




def toPay(request):
    # 支付
    # 获取请求参数
    aid = request.GET.get("address",'-1')
    aid = int(aid)
    addrObj = models.Address.objects.get(id=aid)


    payway = request.GET.get('payway','')


