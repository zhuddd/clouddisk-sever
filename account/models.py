from django.db import models
from django.utils.timezone import localtime


# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=64, verbose_name="邮箱")
    password = models.CharField(max_length=64)
    registration_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    total_size = models.BigIntegerField(verbose_name="总空间", default=1024*1024*1024*10)

    def dict(self):
        return {"Id": self.id, "Email": self.email, "Password": self.password,
                "RegistrationTime": localtime(self.registration_time)}

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

class Captcha(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    captcha = models.CharField(max_length=6, verbose_name="验证码")
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")

    def dict(self):
        return {"Email": self.user.email, "Captcha": self.captcha, "SendTime": localtime(self.send_time)}

    def __str__(self):
        return f"{self.user} {self.captcha}"

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = "验证码"