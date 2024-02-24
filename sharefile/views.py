from datetime import datetime
from time import strptime

from django.shortcuts import render

from account.models import User
from file.models import FileUser
from sharefile.models import ShareList
from utils.LoginCheck import LoginCheck
from utils.MyResponse import MyResponse
from utils.file import file_copy
from utils.randomString import random_string


# Create your views here.

@LoginCheck
def newShare(request):
    user_id = request.user_id
    file_id = request.POST['file_id']
    end_time = request.POST['end_time']
    pwd = request.POST['pwd']
    if end_time == "":
        end_time = "9999-12-31 23:59:59"
    else:
        end_time = end_time + " 23:59:59"
    user = User.objects.get(id=user_id)
    file = FileUser.objects.get(id=file_id, user_id=user_id, is_delete=False, is_uploaded=True)
    code = random_string(16)
    while len(ShareList.objects.filter(share_code=code)) > 0:
        code = random_string(16)
    obj = ShareList.objects.create(user=user, file=file, share_code=code, share_pwd=pwd, share_end_time=end_time)

    return MyResponse.SUCCESS({"share_code": obj.share_code, "end_time": obj.share_end_time, "pwd": obj.share_pwd})


def getShare(request, code):
    try:
        share = ShareList.objects.get(share_code=code, is_delete=False, share_end_time__gte=datetime.now())

        password=""
        if share.share_pwd is not None and share.share_pwd != "":
            if request.method == "GET":
                return render(request, "share_save.html",
                              {"password_required": True})
            password = request.POST['password']
            if password != share.share_pwd:
                return render(request, "share_save.html", {"password_required": True})
        link = f"cloud://code={code}&pwd={password}"
        return render(request, "share_save.html", {
            "name": share.file.file_name,
            "link": link,
            "poster": f"../../file/poster/{code}"})
    except:
        return render(request, "share_lost.html")

@LoginCheck
def shareSave(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    try:
        user_id = request.user_id
        code = request.POST["code"]
        parent_id = request.POST["parent"]
        pwd = request.POST["pwd"]
        if parent_id != "0":
            p = FileUser.objects.filter(user_id=user_id, id=parent_id)
            if p.count() == 0:
                return MyResponse.ERROR("文件夹不存在")
            parent = p[0].id
        else:
            parent = 0
        share = ShareList.objects.get(share_code=code, is_delete=False, share_end_time__gte=datetime.now(), share_pwd=pwd)
        print("share.file.file_id", share.file.id)
        p = parent
        while p != 0:
            if p == share.file.id:
                return MyResponse.ERROR("不能保存到自身")
            p = FileUser.objects.get(user_id=user_id, id=p, is_delete=False, is_uploaded=True).parent_folder
        code = file_copy(user_id, share.file.id, parent)
        if code == 1:
            return MyResponse.SUCCESS("保存成功")
        elif code == 0:
            return MyResponse.ERROR("空间不足")
        else:
            return MyResponse.ERROR("保存失败")
    except:
        return MyResponse.ERROR("保存失败")
