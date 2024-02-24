from django.db import models

from account.models import User
from file.models import FileUser


# Create your models here.

class ShareList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="分享用户")
    file = models.ForeignKey(FileUser, on_delete=models.SET_NULL, verbose_name="分享文件", null=True)
    share_code = models.CharField(max_length=16, verbose_name="分享码")
    share_pwd = models.CharField(max_length=16, verbose_name="分享密码")
    share_time = models.DateTimeField(auto_now_add=True, verbose_name="分享时间")
    share_end_time = models.DateTimeField(verbose_name="分享结束时间")
    is_delete = models.BooleanField(verbose_name="是否删除", default=False)

    class Meta:
        verbose_name = "分享列表"
        verbose_name_plural = "分享列表"

    def dict(self) -> dict:
        return {"Id": self.id, "user_id": self.user.id, "file_id": self.file.id, "share_code": self.share_code,
                "share_pwd": self.share_pwd, "share_time": self.share_time.now().strftime("%Y-%m-%d %H:%M:%S"),
                "share_end_time": self.share_end_time.now().strftime("%Y-%m-%d %H:%M:%S")}

    def __str__(self):
        return f"{self.id}|{self.share_code}"
