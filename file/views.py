from asgiref.sync import sync_to_async
from django.http import FileResponse
from django.shortcuts import render

from file.models import FileUser
from utils import file, Face, KV
from utils.MyResponse import MyResponse
from sever.settings import STATIC_FILES_DIR_FACE
from utils.LoginCheck import LoginCheck, AsyncLoginCheck
from utils.account import get_user_by_session
from utils.file import file_copy, file_delete, getUsedStorage, gettotalSize
from utils.filePreview import all_preview, preview_box, preview_poster


@LoginCheck
def filedir(request, t, msg):
    '''
    获取文件目录
    :param request:
    :return:
    '''
    if request.method == "GET":
        user_id = request.user_id
        # user_id = 1
        data = file.get_file_user_list(user_id, t, msg)
        return MyResponse.SUCCESS(data)
    else:
        return MyResponse.ERROR("请求方式错误")


@LoginCheck
def getface(request, k, t):
    user_id = request.user_id
    # user_id = 2
    user_file = FileUser.objects.get(user_id=user_id, id=k)
    try:
        md5 = user_file.file.hash
        if user_file.file_face is None:
            user_file.file_face = Face.creatFace(md5)
            user_file.save()
        if user_file.file_face:
            return FileResponse(open(STATIC_FILES_DIR_FACE / f"{md5}.{t}", 'rb'))
        else:
            return FileResponse()
    except:
        user_file.file_face = False
        user_file.save()
        return FileResponse()


@LoginCheck
def delete(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    try:
        user_id = request.user_id
        user_file = request.POST["id"]
        files = FileUser.objects.filter(user_id=user_id, id=user_file)
        if files.count() == 0:
            return MyResponse.ERROR("文件不存在")
        if file_delete(user_id, user_file):
            return MyResponse.SUCCESS("删除成功")
        else:
            return MyResponse.ERROR("删除失败")
    except:
        return MyResponse.ERROR("请求参数错误")


@LoginCheck
def rename(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    try:
        user_id = request.user_id
        user_file = request.POST["id"]
        name = request.POST["name"]
        files = FileUser.objects.filter(user_id=user_id, id=user_file)
        if files.count() == 0:
            return MyResponse.ERROR("文件不存在")
        file = files[0]
        file.file_name = name
        file.save()
        return MyResponse.SUCCESS("修改成功")
    except:
        return MyResponse.ERROR("请求参数错误")


@LoginCheck
def paste(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    try:
        user_id = request.user_id
        user_file = request.POST["id"]
        parent_folder = request.POST["parent"]
        files = FileUser.objects.filter(user_id=user_id, id=user_file, is_delete=False, is_uploaded=True)
        if files.count() == 0:
            return MyResponse.ERROR("源文件不存在")
        if parent_folder != "0":
            p = FileUser.objects.filter(user_id=user_id, id=parent_folder)
            if p.count() == 0:
                return MyResponse.ERROR("文件夹不存在")
            parent = p[0].id
        else:
            parent = 0
        file = files[0]
        p = parent
        while p != 0:
            if p == file.id:
                return MyResponse.ERROR("不能粘贴到自身")
            p = FileUser.objects.get(user_id=user_id, id=p, is_delete=False, is_uploaded=True).parent_folder
        code = file_copy(user_id, file.id, parent)
        if code == 1:
            return MyResponse.SUCCESS("修改成功")
        elif code == 0:
            return MyResponse.ERROR("空间不足")
        else:
            return MyResponse.ERROR("修改失败")
    except:
        return MyResponse.ERROR("请求参数错误")


@LoginCheck
def newfolder(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    try:
        user_id = request.user_id
        parent_folder = request.POST["parent"]
        name = request.POST["name"]
        if parent_folder != "0":
            p = FileUser.objects.filter(user_id=user_id, id=parent_folder)
            if p.count() == 0:
                return MyResponse.ERROR("文件夹不存在")
            parent = p[0].id
        else:
            parent = 0
        FileUser.objects.create(file_face=False, file_name=name, file_type="folder",
                                parent_folder=parent, is_folder=True, user_id=user_id,
                                is_uploaded=True)
        return MyResponse.SUCCESS("修改成功")
    except:
        return MyResponse.ERROR("请求参数错误")


@LoginCheck
def usedStorage(request):
    if request.method != "GET":
        return MyResponse.ERROR("请求方式错误")
    try:
        # user_id = 2
        user_id = request.user_id
        used = getUsedStorage(user_id)
        if used is None:
            used = 0
        total = gettotalSize(user_id)
        return MyResponse.SUCCESS({"used": used, "total": total})
    except Exception as e:
        print(e)
        return MyResponse.ERROR("请求参数错误")


@LoginCheck
def getPreviewKey(request):
    if request.method != "GET":
        return MyResponse.ERROR("请求方式错误")
    try:
        user_id = request.user_id
        file_id=request.GET["file_id"]
        key = KV.newKey({"user_id": user_id,"file_id":file_id}, 60*60*24)
        return MyResponse.SUCCESS(key)
    except Exception as e:
        print(e)
        return MyResponse.ERROR("请求参数错误")


async def preview(request, k):
    """预览文件"""

    try:
        s=KV.getKey(k)
        user_id=s["user_id"]
        file_id=s["file_id"]
        return await preview_box(request, user_id,file_id,k)
    except Exception as e:
        print(e)
        return (
            render(request, 'urllose.html'))

async def data(request, k):
    """以流媒体的方式响应视频文件"""
    try:
        s=KV.getKey(k)
        if s is None:
            return MyResponse.ERROR("参数错误")
        k=s["user_id"]
        f=s["file_id"]
        return await all_preview(request, k, f)
    except Exception as e:
        print(e)
        return MyResponse.ERROR("参数错误")

async def poster(request, k):
    """以流媒体的方式响应视频文件"""
    try:
        s=KV.getKey(k)
        if s is None:
            return MyResponse.ERROR("参数错误")
        k=s["user_id"]
        f=s["file_id"]
        return await preview_poster(k, f)
    except Exception as e:
        print(e)
        return FileResponse()


def t(request):
    s = KV.newKey({"a": 1, "b": 2, "c": 3}, 0)
    return MyResponse.SUCCESS({"k": s[0], "v": s[1]})


def t2(request, k):
    s = KV.getKey(k)
    print(s.values())
    return MyResponse.SUCCESS({"k": "s.__dict__", "v": s.get_expiry_age()})
