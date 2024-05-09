from django import forms
from django.contrib import admin

from pay.models import Menu, UserOrders


# Register your models here.
@admin.register(Menu)
class MyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "storage_size","storage_unit","price","max_num","valid_time", "start_time", "end_time")
    search_fields = ("id", "title")
    list_filter = ("price", "valid_time", "start_time", "end_time")


@admin.register(UserOrders)
class MyAdmin(admin.ModelAdmin):
    list_display = ("id","trade_no", "user", "menu", "order_time", "is_pay", "pay_time", "valid_time", "is_valid", "is_delete","refund")
    search_fields = ("id","trade_no", "user", "menu","refund")
    list_filter = ("is_pay", "valid_time", "is_valid", "is_delete","refund")
    readonly_fields=("id","trade_no", "user", "menu", "order_time", "pay_time", "valid_time","call_back")