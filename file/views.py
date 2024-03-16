import os

from django.http import FileResponse
from django.shortcuts import render

from file.models import FileUser
from sever import settings
from sharefile.models import ShareList
from utils import file, Face, KV
from utils.CommonLog import log
from utils.MyResponse import MyResponse
from sever.settings import STATIC_FILES_DIR_FACE
from utils.LoginCheck import LoginCheck
from utils.file import file_copy, file_delete, getUsedStorage, gettotalSize
from utils.filePreview import all_preview, preview_box


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
def folderList(request):
    if request.method == "GET":
        user_id = request.user_id
        # user_id = 1
        data = FileUser.objects.filter(user_id=user_id, is_delete=False, is_uploaded=True, is_folder=True)
        data = [{"id": i.id, "name": i.file_name, "parent": i.parent_folder} for i in data]
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
        log.warning(f"获取/生成文件封面失败，文件id：{k}")
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
        log.warning(f"用户尝试删除文件失败，用户id：{request.user_id},{request.POST}")
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
        log.warning(f"用户尝试重命名文件失败，用户id：{request.user_id},{request.POST}")
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
        log.warning(f"用户尝试粘贴文件失败，用户id：{request.user_id},{request.POST}")
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
        f = FileUser.objects.create(file_face=False, file_name=name, file_type="folder",
                                    parent_folder=parent, is_folder=True, user_id=user_id,
                                    is_uploaded=True)
        return MyResponse.SUCCESS(f.id)
    except:
        log.warning(f"用户尝试新建文件夹失败，用户id：{request.user_id},{request.POST}")
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
    except:
        log.warning(f"用户尝试获取已使用空间失败，用户id：{request.user_id}")
        return MyResponse.ERROR("请求参数错误")


@LoginCheck
def getPreviewKey(request):
    if request.method != "GET":
        return MyResponse.ERROR("请求方式错误")
    try:
        user_id = request.user_id
        file_id = request.GET["file_id"]
        key = KV.newKey({"user_id": user_id, "file_id": file_id}, 60 * 60 * 24)
        return MyResponse.SUCCESS(key)
    except:
        log.warning(f"用户尝试获取预览文件key失败，用户id：{request.user_id},{request.GET}")
        return MyResponse.ERROR("请求参数错误")


async def preview(request, k):
    """预览文件"""

    try:
        s = KV.getKey(k)
        user_id = s["user_id"]
        file_id = s["file_id"]
        return await preview_box(request, user_id, file_id, k)
    except:
        log.warning(f"用户尝试预览文件失败：{request.GET},{k}")
        return (
            render(request, 'urllose.html'))


async def data(request, k):
    """以流媒体的方式响应视频文件"""
    try:
        s = KV.getKey(k)
        if s is None:
            return MyResponse.ERROR("参数错误")
        k = s["user_id"]
        f = s["file_id"]
        return await all_preview(request, k, f)
    except:
        log.warning(f"用户尝试预览文件内容失败：{request.GET},{k}")
        return MyResponse.ERROR("参数错误")


def poster(request, k):
    try:
        s = KV.getKey(k)
        if s.get("user_id") is not None and s.get("file_id") is not None:
            file = FileUser.objects.get(user_id=s["user_id"], id=s["file_id"], is_delete=False, is_uploaded=True)
            path = settings.STATIC_FILES_DIR_FACE / f'{file.file.hash}.preview'
            if path.exists():
                return FileResponse(open(path, 'rb'), filename=f'{file.file_name}.png')
        else:
            file = ShareList.objects.get(share_code=k, is_delete=False).file
            try:
                file_hash = file.file.hash
            except:
                file_hash = ""
            name = file.file_name
            path = settings.STATIC_FILES_DIR_FACE / f'{file_hash}.preview'
            if os.path.exists(path):
                return FileResponse(open(path, 'rb'), filename=f'{name}.png')
        file_type = file.file_type
        return FileResponse(open(settings.ICON_DIR / f'{file_type}.svg', 'rb'),
                            filename=f'{file_type}.svg')
    except Exception as e:
        log.warning(f"用户尝试获取文件封面失败{request.GET},{k},{e}")
        return FileResponse()
