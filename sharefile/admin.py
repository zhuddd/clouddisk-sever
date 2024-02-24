from django.contrib import admin

from sharefile.models import ShareList


# Register your models here.
@admin.register(ShareList)
class MyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "file", "share_code", "share_pwd", "share_time", "share_end_time", "is_delete")
    search_fields = ("id", "user__id", "file__id", "share_code", "share_pwd")