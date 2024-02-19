from django.db import models

# Create your models here.
from account.models import User


class Files(models.Model):
    hash = models.CharField(max_length=64, verbose_name="文件hash")
    check_hash = models.CharField(max_length=64, verbose_name="验证hash")
    size = models.BigIntegerField(verbose_name="文件大小")
    upload_size = models.BigIntegerField(verbose_name="已上传大小", default=0)
    broken = models.BooleanField(verbose_name="是否损坏", default=True)

    def dict(self):
        return {"Id": self.id, "hash": self.hash, "size": self.size, "broken": self.broken}

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = "文件"


class FileUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户id")
    file = models.ForeignKey(Files, on_delete=models.CASCADE, verbose_name="目标文件", null=True)
    file_face = models.BooleanField(verbose_name="是否有文件封面", null=True)
    file_name = models.CharField(max_length=255, verbose_name="文件名")
    file_type = models.CharField(max_length=64, verbose_name="文件类型")
    parent_folder = models.IntegerField(verbose_name="父文件夹")
    is_folder = models.BooleanField(verbose_name="是否为文件夹")
    is_uploaded = models.BooleanField(verbose_name="是否已上传", default=False)
    is_delete = models.BooleanField(verbose_name="是否删除", default=False)
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    def dict(self) -> dict:
        return dict({"Id": self.id, "file_name": self.file_name, "file_type": self.file_type,
                     "user_id": self.user.id, "parent_folder": self.parent_folder, "is_folder": self.is_folder,
                     "is_delete": self.is_delete, "file_face": self.file_face, "upload_time": self.upload_time.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "size":self.file.size if self.file else 0})

    def tree_dict(self) -> dict:
        return dict(
            {"Id": self.id, "file_name": self.file_name, "file_type": self.file_type, "is_folder": self.is_folder})

    def __str__(self):
        return f"{self.id}|{self.file_name}"

    class Meta:
        verbose_name = "用户文件"
        verbose_name_plural = "用户文件"