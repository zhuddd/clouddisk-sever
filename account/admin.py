from django.contrib import admin

from account.models import User, Captcha


# Register your models here.
@admin.register(User)
class MyAdmin(admin.ModelAdmin):
    # list_display = 你需要展示的字段应该写在这里,此处是数据库中的字段
    list_display = ("id", "email", "registration_time")
    search_fields = ("id", "email")

@admin.register(Captcha)
class MyAdmin(admin.ModelAdmin):
    list_display = ("user", "captcha", "send_time")
    search_fields = ("user__id", "user__email", "send_time")