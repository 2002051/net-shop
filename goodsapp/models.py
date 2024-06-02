from django.db import models
import collections

# Create your models here.

# 类别表
class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __str__(self):
        return self.cname


class Goods(models.Model):
    # 商品表
    gname = models.CharField(max_length=100, unique=True)
    gdesc = models.CharField(max_length=100)  # 商品描述
    oldprice = models.DecimalField(max_digits=5,decimal_places=2)  # 原价格，用浮点，总长度五位精度为2
    price = models.DecimalField(max_digits=5,decimal_places=2)  # 现价，用浮点，总长度五位精度为2
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.gname
    def getColorImg(self):   #调用此方法来获取商品图片
        return self.inventory_set.first().color.colorurl

    def getColors(self):
        colors = []
        for inventory in self.inventory_set.all():      # 遍历该商品的每一个库存
            color = inventory.color
            if color not in colors:  # 如果颜色列表中没有该库存的颜色，
                colors.append(color)    #新的库存颜色压入列表。而且不会重复
        return colors  #最终把所有本商品的其它库存颜色都展示在colors里。

    def getSize(self):  #获取商品的所有尺码
        sizes = []
        for inventory in self.inventory_set.all():
            color = inventory.size
            if color not in sizes:
                sizes.append(color)
        return sizes

    def getDetailInfo(self):# 获取商品详情
            datas = collections.OrderedDict()  #创建一个有序字典，用于存放商品的详情信息。
            # 遍历当前商品的所有详情信息。
            for detail in self.gooddetail_set.all():
                #获取详情名称（参数规格，整体款式，模特实拍）
                gdname = detail.getName()
                # 判断当前详情名称是否在字典中存在
                if gdname not in datas:
                    datas[gdname] = [detail.gdurl]
                else:
                    datas[gdname].append(detail.gdurl)
            return datas

    #商品描述
class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

# 商品
class GoodDetail(models.Model):
    gdurl = models.ImageField(upload_to="") #为空就默认采用media下的目录
    goodsdname = models.ForeignKey(GoodsDetailName,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

    def getName(self):
        return self.goodsdname.gdname

class Size(models.Model):
    sname = models.CharField(max_length=10)


class Color(models.Model):  #商品的其它颜色
    colorname = models.CharField(max_length=10)
    colorurl = models.ImageField(upload_to="color/")  #表示图片路径在media下面的 color文件夹下面


class Inventory(models.Model):
    #商品库存
    count = models.PositiveIntegerField(default=100)# 正整数,默认库存100件
    color = models.ForeignKey(Color,on_delete=models.CASCADE) # 颜色
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE) # 商品信息
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
