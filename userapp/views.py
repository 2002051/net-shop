from io import BytesIO

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse

from cartapp.cartmanager import SessionCartManager
from userapp import models
from utils.encrypt import md5
import jsonpickle

# Create your views here.
def RegisterView(request):
    if request.method == "GET":
        return render(request, 'register.html')

    # 获取请求参数
    account = request.POST.get('account')
    pwd = request.POST.get('password')
    pwd = md5(pwd)  # 加 密

    # 将用户名插入到数据库中,并用变量接收这个返回值
    user = models.UserInfo.objects.create(uname=account, pwd=pwd)

    # 判断注册成功与否
    if user:
        # 将当前注册的用户对象保存到全局上下文session中其实就是django创建的一个数据表，django-session中间
        request.session['user'] = jsonpickle.dumps(user)  # 保存到session缓存中

        return redirect("/user/center/")  # 跳转到主页面

    return redirect('/user/register/')


def CenterView(request):
    # 用户中心
    if request.method == "GET":
        return render(request, 'center.html')


def LoginView(request):
    #     用户登录
    if request.method == "GET":
        red = request.GET.get('redirct','')

        return render(request, "login.html",{'red':red,'cartitems':request.GET.get('cartitems','')})
    # post 请求
    # 获取post请求参数

    uname = request.POST.get('account', '')
    pwd = request.POST.get('password', '')
    redi = request.POST.get('redirect','') # 获取隐藏域value值

    # print(uname, pwd)
    # 去数据库中查询用户是否存在.
    userlist = models.UserInfo.objects.filter(uname=uname, pwd=pwd)

    # 判断登录成功,成功了那么这个对象就存在
    if userlist:
        request.session['user'] = jsonpickle.dumps(userlist[0]) # 把数据存到session中,表示登录成功
        SessionCartManager(request.session).migrateSession2DB()
        if redi == 'cart':  # 说明用户通过购物车页面进行登录
             # 将session中的购物项转移到数据表中间


            return redirect('/cart/queryAll')
        elif redi == "order":  # 表示从订单模块来到

            return redirect('/order/toOrder/?cartitems='+request.POST.get('cartitems'))

        return redirect('/user/center/')
    else:

        return redirect('/user/login/')


from utils.code import *


def loadCode(request):
    # 图片src的请求也是get请求
    if request.method == "GET":
        # 调用工具包下的函数来生成验证码
        img, txt = check_code()

        # 把验证码的 字符串保存到全局上下文session中以便在其它全局函数进行调用
        request.session['sessionCode'] = txt
        print(txt)
        stream = BytesIO()  # 创建一个内存中的文件
        img.save(stream, 'png')  # 然后把图片写到这个内存中去，然后

        # 响应到页面
        return HttpResponse(stream.getvalue())


def CheckCode(request):
    if request.method == "GET":
        # 获取ajax请求参数
        code = request.GET.get('code', '')
        # 获取系统生成验证码的值
        sessioncode = request.session.get("sessionCode")

        flag = code == sessioncode  # 如果输入的验证码正确,值就是true,错误就是false
        return JsonResponse({'flag': flag})


def logout(request):
    # 退出登录
    # 清空session中的 所有 数据
    request.session.clear()

    return redirect("/user/login/")


from django.core.serializers import serialize


def address(request):
    if request.method == "GET":
        # 查询当前用户的所有地址列表
        user = jsonpickle.loads(request.session.get('user'))
        addrlist = user.address_set.all()



        return render(request, 'address.html',{"addrlist":addrlist})
    # 获取请求参数：
    print(request.POST)

    params = request.POST.dict()

    params.pop('csrfmiddlewaretoken')

    # 当前登录用户信息
    user = jsonpickle.loads(request.session.get('user'))
    #                                                                如果已经写过地址在数据库，那么此地址就不作默认地址
    models.Address.objects.create(userinfo =user,isdefault=(lambda count:True if count==0 else False)(user.address_set.count())  ,**params)



    return redirect('/user/address/')

def loadAddr(request):  # 获取区域信息
    # 获取请求参数

    pid = request.GET.get('pid', -1)
    pid = int(pid)
    print(pid)
    # 根据父id查询区划信息
    arealist = models.Area.objects.filter(parentid=pid)

    # 序列化 arealist
    jarealist = serialize('json', arealist)

    return JsonResponse({'jarealist': jarealist})
