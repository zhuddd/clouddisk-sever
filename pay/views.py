import json
from datetime import datetime, timedelta

from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeRefundRequest import AlipayTradeRefundRequest
from django.contrib.admin.views.decorators import staff_member_required
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from django.shortcuts import render
from django.utils.timezone import localtime

from pay.models import UserOrders, Menu
from sever import settings
from utils.CommonLog import log
from utils.LoginCheck import LoginCheck
from utils.MyResponse import MyResponse
from utils.account import get_user_by_session
from utils.aliPay import alipayConfig, alipayModel, check_pay, add_day, refundModel


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
        log.warning(f"套餐未找到：{menu_id}")
        menu = Menu.objects.get(id=menu_id)
    except:
        return MyResponse.ERROR("menu is not exist")
    return MyResponse.SUCCESS(menu.text)


@LoginCheck
def pay(request):
    data = request.GET
    # user_id = 1
    user_id = request.user_id
    menu_id = data.get("menu_id")
    if not menu_id:
        log.warning(f"创建订单时，套餐未找到：{menu_id}")
        return MyResponse.ERROR("menu is required")
    try:
        menu = Menu.objects.get(id=menu_id)
    except:
        log.warning(f"创建订单时，套餐未找到：{menu_id}")
        return MyResponse.ERROR("menu is not exist")
    order = UserOrders.objects.create(user_id=user_id, menu=menu)
    alipay_client_config = alipayConfig()
    price = f'{float(menu.price) / 100:.2f}'

    model = alipayModel(order.id, price, menu.title)
    payrequest = AlipayTradePagePayRequest(biz_model=model)
    payrequest.notify_url = settings.CALLBACK  # 通知地址
    try:
        client = DefaultAlipayClient(alipay_client_config)
        response_content = client.page_execute(payrequest, http_method="GET")
    except :
        log.warning(f"支付链接创建失败：{order.id}")
        return MyResponse.ERROR("pay error")
    if not response_content:
        log.warning(f"支付链接创建失败：{order.id}")
        return MyResponse.ERROR("pay error")
    else:
        valid_time = f'{menu.valid_time}天' if menu.valid_time != -1 else "永久有效"
        d = {
            "id": order.id,
            "title": menu.title,
            "info": f"容量：{menu.storage_size} {menu.get_storage_unit_display()} \n价格：{price} \n有效时间：{valid_time}",
            "price": f'{float(menu.price) / 100:.2f}元',
            "url": response_content

        }
        return MyResponse.SUCCESS(d)


@LoginCheck
def paysuccess(request):
    order_id = request.GET.get("order_id")
    if not order_id:
        return MyResponse.ERROR("order_id is required")
    try:
        order = UserOrders.objects.get(id=order_id, user_id=request.user_id)
        if order.is_pay:
            return MyResponse.SUCCESS(True)
        return MyResponse.SUCCESS(False)
    except:
        log.warning(f"订单未找到：{order_id}, user_id:{request.user_id}")
        return MyResponse.ERROR("order is not exist")

def history(request):
    k=request.GET.get('k')
    if not k:
        return render(request, "404.html")
    user_id=get_user_by_session(k)
    if not user_id:
        return render(request, "404.html")
    items=UserOrders.objects.filter(user_id=user_id).order_by('-order_time')
    for i in range(len(items)):
        items[i].is_pay = '已支付' if items[i].is_pay else '未支付'
        items[i].is_valid = '有效' if items[i].is_valid else ('无效(已退款)' if items[i].refund else '无效(未退款)')
        items[i].menu.price = f'{float(items[i].menu.price) / 100:.2f}元'
    return render(request, "pay_history.html",{'items':items})

def callback(request):
    try:
        if request.method != 'POST':
            return MyResponse.ERROR("error")
        params = request.POST.dict()  # 获取参数字典
        if not check_pay(params):
            return MyResponse.ERROR('')
        order = UserOrders.objects.get(id=params["out_trade_no"])
        menu = order.menu
        user = order.user
        order.trade_no = params["trade_no"]
        order.is_pay = True
        order.pay_time = params["gmt_payment"]
        if order.menu.valid_time > 0:
            order.valid_time = add_day(params["gmt_payment"], order.menu.valid_time)
        else:
            order.valid_time = order.menu.end_time
        order_len = UserOrders.objects.filter(user=user, menu=menu, is_valid=True).count()
        if 0 < menu.max_num <= order_len:
            order.is_valid = False
            alipay_client_config = alipayConfig()
            refund_model = refundModel(order.id, f'{float(menu.price) / 100:.2f}', "购买次数超限")
            refund_request = AlipayTradeRefundRequest(biz_model=refund_model)
            client = DefaultAlipayClient(alipay_client_config)
            res = client.execute(refund_request)
            try:
                res = json.loads(res)
                if res['msg'] == 'Success':
                    log.warning(f"超出限购数量,退款成功：{order.id}")
                    order.refund = True
                else:
                    log.warning(f"超出限购数量,退款失败：{order.id}")
                    order.refund = False
            except:
                log.warning(f"超出限购数量,退款失败：{order.id}")
                order.refund = False
        else:
            order.is_valid = True
        order.call_back = str(params)
        order.save()
        return MyResponse.SUCCESS('success')
    except :
        log.warning(f"支付回调失败：{request.params}")
        return MyResponse.ERROR("error")


@staff_member_required
def admin(request):
    return render(request, "pay.html")


@staff_member_required
def income(request):
    before_7_day = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
    objs = UserOrders.objects.filter(is_pay=True, is_valid=True, pay_time__gte=before_7_day)
    r = []
    date = {}
    menus = {}
    menus2 = {}
    for i in range(6, -1, -1):
        t = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        date[t] = 0
    for obj in objs:
        t = localtime(obj.order_time).strftime('%Y-%m-%d')
        date[t] += obj.menu.price / 100
        try:
            menus[obj.menu.title] += obj.menu.price
            menus2[obj.menu.title] += 1
        except:
            menus[obj.menu.title] = obj.menu.price
            menus2[obj.menu.title] = 1
    r.append([[k for k in date.keys()], [v for v in date.values()]])
    r.append([{"name": f"{k}\n{v / 100:.2f}元", "value": v} for k, v in menus.items()])
    r.append([{"name": f"{k}\n{v}份", "value": v} for k, v in menus2.items()])

    return MyResponse.SUCCESS(r)
