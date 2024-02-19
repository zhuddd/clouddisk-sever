# Create your views here.
import json
import os

from django.http import JsonResponse

from utils.file import get_file_hash_file, check_file, get_file_from_model, getUsedStorage, set_file_user, gettotalSize
from file.models import Files, FileUser
from account.models import  User
from sever import settings
from utils.LoginCheck import LoginCheck
from utils.MyResponse import MyResponse


@LoginCheck
def creat_contents(request):
    if request.method != 'POST':
        return MyResponse.ERROR("请求方式错误")
    data = request.POST
    tree = data.get('tree')
    p = data.get('p', 0)
    user_id = request.user_id
    if not tree:
        return MyResponse.ERROR("参数错误")
    try:
        tree = json.loads(tree)
        dic = set_file_user(user_id, p, tree)
        return MyResponse.SUCCESS(dic)
    except:
        return MyResponse.ERROR("参数错误2")


@LoginCheck
def upload_check(request):
    if request.method != 'POST':
        return MyResponse.ERROR("请求方式错误")
    data = request.POST
    file_hash = data.get('hash')
    check_hash = data.get('check_hash')
    size = data.get('size')
    f_id = data.get('f_id')
    user_id = request.user_id
    if not file_hash or not check_hash or not size:
        return MyResponse.ERROR("参数错误")
    usedSize = getUsedStorage(user_id)
    totalSize = gettotalSize(user_id)
    if usedSize + int(size) > totalSize:
        return MyResponse.ERROR("空间不足")
    file = Files.objects.filter(hash=file_hash, size=size, check_hash=check_hash)
    if len(file) > 0:
        file = file[0]
        if f_id:
            user_file = FileUser.objects.filter(id=f_id, user_id=user_id, is_delete=False)
            if len(user_file) == 0:
                return MyResponse.SUCCESS({"message": "文件已存在", "state": -2})
            user_file = user_file[0]
            user_file.file = file
            user_file.is_uploaded = True
            user_file.save()
        if file.upload_size < file.size:
            return MyResponse.SUCCESS({"message": "文件已存在", "state": 2, "start_byte": file.upload_size})
        return MyResponse.SUCCESS({"message": "文件已存在", "state": 1})
    else:
        return MyResponse.SUCCESS({"message": "文件不存在", "state": 3})


@LoginCheck
def upload_view(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    metadata = request.FILES.get('metadata')
    upload_file = request.FILES.get('file')
    if metadata:
        metadata_dict = json.loads(metadata.read().decode('utf-8'))
        start_byte = metadata_dict.get('start_byte')
        chunk_size = metadata_dict.get('chunk_size')
        chunk_hash = metadata_dict.get('chunk_hash')
        file_size = metadata_dict.get('size')
        file_hash = metadata_dict.get('hash')
        file_check_hash = metadata_dict.get('check_hash')
        if start_byte is None or not chunk_size or not chunk_hash or not file_hash or not file_check_hash:
            return MyResponse.ERROR("参数错误")
        file_model = get_file_from_model(file_hash, file_check_hash, file_size)
        file_path = (settings.STATIC_FILES_DIR_FILE / file_hash).absolute()  # 更改文件保存路径
        if not file_model.broken:
            if check_file(file_hash):
                return MyResponse.ERROR('文件已存在')
            else:
                file_model.broken = True
        mode = 'wb' if start_byte == 0 else 'ab'  # 如果文件不存在则创建新文件，存在则以追加模式续写
        if chunk_hash != get_file_hash_file(upload_file):
            return MyResponse.ERROR('文件损坏')
        with open(file_path, mode) as destination:
            if upload_file:
                # 移动文件指针到指定位置开始写入
                upload_file.seek(start_byte)
                for chunk in upload_file.chunks():
                    destination.write(chunk)
        size = os.path.getsize(file_path)
        file_model.upload_size = size
        file_model.save()
        return MyResponse.SUCCESS('上传成功')
    else:
        return MyResponse.ERROR("参数错误")
