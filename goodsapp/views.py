from django.shortcuts import render
from goodsapp import models
from django.core.paginator import Paginator  # 分页器导入

# Create your views here.
from utils.pagination import Pagination


def IndexView(request, cid=6, num=1):
    if request.method == "GET":
        cid = cid
        num = int(num)
        # 查询所有类别信息 Category
        categorylist = models.Category.objects.all()

        # 查询当前类别下的所有商品信息
        goodslist = models.Goods.objects.filter(category_id=cid).order_by("id")

        # 创建分页器对象
        # paginator_obj = Paginator(goodslist,8)# 每页八条记录
        page_object = Pagination(request, goodslist, page_size=8)

        # 获取某页数据
        # page_obj = paginator_obj.page(num)

        return render(request, 'index.html',
                      {'categorylist': categorylist, "cid": cid, "goodlist": page_object.page_queryset,
                       "page_string": page_object.html()})


def recommend_view(func):  # 定义装饰器
    def wrapper(request, gid, *args, **kwargs):
        # 从cookie中获取访问的所有商品id
        c_goodsid = request.COOKIES.get('rem','')


        # 存放用户访问商品的goodsid列表
        goodsidlist = [goodsid for goodsid in c_goodsid.split() if goodsid.strip()]


        # 最终推荐商品列表
        goodsobjectlist = [ models.Goods.objects.get(id=vgoodsid) for vgoodsid in goodsidlist if models.Goods.objects.get(id=vgoodsid).category_id == models.Goods.objects.get(id=gid).category_id and vgoodsid != gid][:4]
        # 调用修饰器修饰的函数
        response = func(request, gid, goodsobjectlist, *args, **kwargs)

        #判断用户访问商品是否存在于goodsldlist中

        if gid in goodsidlist:
            goodsidlist.remove(gid)
            goodsidlist.insert(0,gid)
        else:
            goodsidlist.insert(0,gid)



        # 将用户访问的商品id存放至cookie中
        response.set_cookie('rem',' '.join(map(str, goodsidlist)),max_age = 3*24*60*60)
        return response

    return wrapper


@recommend_view
def DetailView(request, gid, recommend_list=[]):
    # 商品细节

    if request.method == "GET":
        goodsid = int(gid)  # 获取商品id
        # 根据商品id查询详细信息
        goods = models.Goods.objects.get(id=goodsid)
        return render(request, 'detail.html', {'goods': goods, 'recommend_list': recommend_list})
