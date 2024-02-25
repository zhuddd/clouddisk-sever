from django.db import models
from django.templatetags.tz import localtime
from mdeditor.fields import MDTextField

from account.models import User


# Create your models here.


##订阅表
class Menu(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    text = MDTextField(verbose_name='内容')
    storage_size = models.IntegerField(verbose_name='存储大小')
    # 添加存储单位选择字段
    STORAGE_UNIT_CHOICES = (
        (1, 'B'),
        (1024, 'KB'),
        (1024 * 1024, 'MB'),
        (1024 * 1024 * 1024, 'GB'),
        (1024 * 1024 * 1024 * 1024, 'TB'),
    )
    storage_unit = models.BigIntegerField(choices=STORAGE_UNIT_CHOICES, default=1024 * 1024 * 1024,
                                          verbose_name='存储单位')
    price = models.IntegerField(verbose_name='价格 (单位：分)')
    max_num = models.IntegerField(verbose_name='单用户限制次数', default=-1)
    valid_time = models.IntegerField(verbose_name='有效时间 (-1永久有效)', default=-1)
    start_time = models.DateField(verbose_name='开始时间')
    end_time = models.DateField(verbose_name='结束时间', default="9999-12-31")

    def __str__(self):
        return self.title

    def dict(self):
        return {"Id": self.id, "Title": self.title, "StorageSize": self.storage_size,
                "storage_unit": self.storage_unit, "Price": self.price, "ValidTime": self.valid_time,
                "StartTime": localtime(self.start_time), "EndTime": localtime(self.end_time)}

    class Meta:
        verbose_name = "订阅"
        verbose_name_plural = "订阅"


class UserOrders(models.Model):
    trade_no = models.CharField(max_length=64, verbose_name="支付宝交易号", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="订阅内容")
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="订阅时间")
    is_pay = models.BooleanField(verbose_name="是否支付", default=False)
    pay_time = models.DateTimeField(verbose_name="支付时间", null=True)
    valid_time = models.DateTimeField(verbose_name="有效时间", null=True)
    is_valid = models.BooleanField(verbose_name="是否有效", default=False)
    is_delete = models.BooleanField(verbose_name="是否删除", default=False)
    call_back = models.TextField(verbose_name="回调数据", null=True)

    def __str__(self):
        return f"用户订单{self.id} 用户{self.user} 订阅{self.menu} 订阅时间{localtime(self.order_time).strftime('%Y-%m-%d %H:%M:%S')} 是否支付{self.is_pay} "

    def dict(self):
        return {"Id": self.id, "UserId": self.user.id, "MenuId": self.menu.id,
                "OrderTime": localtime(self.order_time).strftime("%Y-%m-%d %H:%M:%S"),
                "IsPay": self.is_pay,
                "PayTime": localtime(self.pay_time).strftime("%Y-%m-%d %H:%M:%S") if self.pay_time else None,
                "ValidTime": localtime(self.valid_time).strftime("%Y-%m-%d %H:%M:%S") if self.valid_time else None,
                "IsValid": self.is_valid, "IsDelete": self.is_delete}

    class Meta:
        verbose_name = "用户订单"
        verbose_name_plural = "用户订单"
