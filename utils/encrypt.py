# MD5加密
from django.conf import settings
import hashlib
def md5(data_string):  # data_string表示要加密的字符串
        # salt = "xxxxxxxxx"
        # obj = hashlib.md5(salt.encode("utf-8"))
        obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))   # 用django中setting里面的随机的secrey_key 来当盐加入。
        obj.update(data_string.encode('utf-8'))
        return obj.hexdigest()