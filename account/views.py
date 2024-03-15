import datetime
import random

from account.models import Captcha
from utils.CommonLog import log
from utils.account import *

from utils.MyResponse import MyResponse
from utils.mail import send_mail


def login(request):
    if request.method == "GET":
        data = request.GET
        t = data.get("type", "")
        r = get_account(t, data)
        if r[1]:
            rt = MyResponse.SUCCESS(r[0])
            rt.set_cookie("session", r[0]["session"])
        else:
            rt = MyResponse.ERROR(r[0])
    else:
        rt = MyResponse.ERROR({"error": "请求参数错误"})
    return rt


def register(request):
    if request.method == "POST":
        try:
            data = request.POST
            email = data["email"]
            password = data["password"]
            r = creat_account(email, password)
            if r[1]:
                rt = MyResponse.SUCCESS(r[0])
                rt.set_cookie("session", r[0]["session"])
                log.info(f"注册成功:{request.POST}")
            else:
                rt = MyResponse.ERROR(r[0])
        except:
            log.info(f"注册失败:{request.POST}")
            rt = MyResponse.ERROR({"error": "请求参数错误"})
    else:
        rt = MyResponse.ERROR({"error": "请求参数错误"})
    return rt


def update_password(request):
    if request.method == "POST":
        try:
            data = request.POST
            email = data["email"]
            password = encrypt_password(data["password"])
            captcha = data["captcha"]
            catpchaobj = Captcha.objects.filter(user__email=email, captcha=captcha)
            if not catpchaobj.exists() or (
                    datetime.datetime.now().timestamp() - catpchaobj[0].send_time.timestamp()) > 600:
                return MyResponse.ERROR("验证码错误或已过期")
            catpchaobj[0].delete()
            account = get_account_by_email(email)
            account.password = password
            account.save()
            log.info(f"更新密码成功:{request.POST}")
            rt = MyResponse.SUCCESS("ok")
        except:
            log.info(f"更新密码错误:{request.POST}")
            rt = MyResponse.ERROR("error")
    else:
        rt = MyResponse.ERROR("请求参数错误")
    return rt


def get_captcha(request):
    if request.method == "GET":
        MyResponse.ERROR('error')
    mail = request.POST.get('email')
    if mail == None:
        return MyResponse.ERROR('error')
    userobj = User.objects.filter(email=mail)
    if not userobj.exists():
        return MyResponse.ERROR('用户不存在')
    userobj = userobj[0]
    captchaobj = Captcha.objects.filter(user=userobj)
    code = random.randint(100000, 999999)
    t = datetime.datetime.now()
    if captchaobj.exists():
        captchaobj = captchaobj[0]
        if (t.timestamp() - captchaobj.send_time.timestamp()) < 60:
            return MyResponse.ERROR('60秒内只能发送一次')
        captchaobj.captcha = code
        captchaobj.send_time = datetime.datetime.now()
        captchaobj.save()
    else:
        captchaobj = Captcha()
        captchaobj.user = userobj
        captchaobj.captcha = code
        captchaobj.send_time = t
        captchaobj.save()

    send_mail([mail],
              'Account',
              f'验证码',
              f'您的验证码是:{code}，10分钟内有效。\n\n '
              f'如非本人操作，请忽略本邮件。\n\n '
              f'本邮件由系统自动发出，请勿直接回复！\n\n'
              f'{t.strftime("%Y-%m-%d %H:%M:%S")}'
              )
    log.info(f"将验证码发送至 {mail} code:{code}")
    return MyResponse.SUCCESS("ok")
