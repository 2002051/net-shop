from django.db import models

# Create your models here.
from goodsapp.models import Color, Goods, Size
from userapp.models import UserInfo
import math

class CartItem(models.Model):
    # 购物车列表
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)

    def getColor(self):
        # 获取商品颜色
        return Color.objects.get(id=self.colorid,)

    def getGoods(self):

        return Goods.objects.get(id=self.goodsid)

    def getSize(self):

        return Size.objects.get(id=self.sizeid)


    def getTotalPrice(self):
        return math.ceil(int(self.count) * self.getGoods().price)  # 计算总价,向上四舍五入

