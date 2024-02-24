from datetime import datetime
from time import strptime

from django.shortcuts import render

from account.models import User
from file.models import FileUser
from sharefile.models import ShareList
from utils.LoginCheck import LoginCheck
from utils.MyResponse import MyResponse
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
        link = f"cloud://code={code}"
        if share.share_pwd is not None and share.share_pwd != "":
            if request.method == "GET":
                return render(request, "share_save.html",
                              {"password_required": True})
            password = request.POST['password']
            if password != share.share_pwd:
                return render(request, "share_save.html", {"password_required": True})
            link += f"&pwd={password}"
        return render(request, "share_save.html", {
            "name": share.file.file_name,
            "link": link,
            "poster": f"../../file/poster/{code}"})
    except:
        return render(request, "share_lost.html")
