import random
import time

from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from django.http import HttpResponse, HttpResponseRedirect

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from pay.models import UserOrders, Menu
from sever import settings
from utils.LoginCheck import LoginCheck
from utils.MyResponse import MyResponse
from utils.aliPay import alipayConfig, alipayModel, check_pay, add_day

@LoginCheck
def getMenu(request):
    from datetime import datetime
    # user_id = 1
    user_id = request.user_id
    now = datetime.now()
    menus = Menu.objects.filter(start_time__lte=now, end_time__gte=now)
    r = []
    for menu in menus:
        if menu.max_num > 0:
            if UserOrders.objects.filter(user_id=user_id, menu=menu, is_valid=True).count() >= menu.max_num:
                continue
        r.append(menu.dict())
    return MyResponse.SUCCESS(r)

def getInfo(request):
    data = request.GET
    menu_id = data.get("menu_id")
    if not menu_id:
        return MyResponse.ERROR("menu is required")
    try:
        menu = Menu.objects.get(id=menu_id)
    except:
        return MyResponse.ERROR("menu is not exist")
    return MyResponse.SUCCESS(menu.text)

@LoginCheck
def pay(request):
    # 实例化客户端
    data = request.GET
    # user_id = 1
    user_id = request.user_id
    menu_id = data.get("menu_id")
    if not menu_id:
        return MyResponse.ERROR("menu is required")
    try:
        menu = Menu.objects.get(id=menu_id)
    except:
        return MyResponse.ERROR("menu is not exist")
    order = UserOrders.objects.create(user_id=user_id, menu=menu)
    alipay_client_config = alipayConfig()
    price = f'{float(menu.price) / 100:.2f}'

    model = alipayModel(order.id, price, menu.title)
    payrequest = AlipayTradePagePayRequest(biz_model=model)
    payrequest.notify_url = settings.CALLBACK  # 通知地址
    # 执行API调用
    response_content = False
    try:
        client = DefaultAlipayClient(alipay_client_config)
        response_content = client.page_execute(payrequest, http_method="GET")
    except Exception as e:
        return MyResponse.ERROR(str(e))
    if not response_content:
        return MyResponse.ERROR("pay error")
    else:
        valid_time = f'{menu.valid_time}天' if menu.valid_time != -1 else "永久有效"
        d={
            "id": order.id,
            "title": menu.title,
            "info":f"容量：{menu.storage_size} {menu.get_storage_unit_display()} \n价格：{price} \n有效时间：{valid_time}",
            "price":f'{float(menu.price) / 100:.2f}元',
            "url": response_content

        }
        return MyResponse.SUCCESS(d)

@LoginCheck
def paysuccess(request):
    order_id = request.GET.get("order_id")
    if not order_id:
        return MyResponse.ERROR("order_id is required")
    try:
        order = UserOrders.objects.get(id=order_id,user_id=request.user_id)
        if order.is_pay:
            return MyResponse.SUCCESS(True)
        return MyResponse.SUCCESS(False)
    except:
        return MyResponse.ERROR("order is not exist")


def callback(request):
    try:
        if request.method == 'POST':
            params = request.POST.dict()  # 获取参数字典
            if check_pay(params):
                order = UserOrders.objects.get(id=params["out_trade_no"])
                order.trade_no = params["trade_no"]
                order.is_pay = True
                order.pay_time = params["gmt_payment"]
                if order.menu.valid_time > 0:
                    order.valid_time = add_day(params["gmt_payment"], order.menu.valid_time)
                else:
                    order.valid_time = order.menu.end_time
                order.is_valid = True
                order.call_back = str(params)
                order.save()
                return MyResponse.SUCCESS('success')
        return MyResponse.ERROR('')
    except Exception as e:
        return MyResponse.ERROR("error")
