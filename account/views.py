from utils.account import *

from utils.MyResponse import MyResponse



def login(request):
    rt = None
    if request.method == "GET":
        data = request.GET
        type = data.get("type", "")
        r = get_account(type, data)
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
            else:
                rt = MyResponse.ERROR(r[0])
        except:
            rt = MyResponse.ERROR({"error": "请求参数错误"})
    else:
        rt = MyResponse.ERROR({"error": "请求参数错误"})
    return rt


