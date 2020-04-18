from django.db import models


# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=16)
    userName = models.CharField(max_length=50)
    pwd = models.CharField(max_length=16)
    sexType = [("1", "男"),
               ("2", "女")
               ]
    sex = models.CharField(choices=sexType, max_length=1)
    brith = models.DateField()
    tel = models.CharField(max_length=11)
    address = models.CharField(max_length=30)
    type = [
        ("1", "普通用户"),
        ("2", "管理员"),
        ("3", "经理")
    ]
    userType = models.CharField(choices=type, max_length=1)

    class Meta:
        db_table = "t_user"


class Supplier(models.Model):
    suppId = models.CharField(max_length=32)
    supplierName = models.CharField(max_length=30)
    linkman = models.CharField(max_length=30)  # 联系人
    tel = models.CharField(max_length=11)
    addr = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    desc = models.CharField(max_length=50)
    date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        db_table = "t_supplier"


class Bill(models.Model):
    billId = models.CharField(max_length=32)
    commodityName = models.CharField(max_length=30)
    commodityUnit = models.CharField(max_length=20)
    commodityNum = models.IntegerField()
    sumMoney = models.IntegerField()
    datetime = models.DateTimeField(blank=True, auto_now=True)
    type = [
        ("1", "未付款"),
        ("2", "已付款")
    ]
    isPay = models.CharField(choices=type, max_length=1)
    # 外键的设置不需要添加_id，默认在名字后自动添加_id
    supp = models.ForeignKey(to=Supplier, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = "t_bill"

