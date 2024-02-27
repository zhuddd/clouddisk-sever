# Create your views here.
import json
import os

from django.http import JsonResponse

from utils.file import get_file_hash_file, check_file, get_file_from_model, getUsedStorage, set_file_user, gettotalSize
from file.models import Files, FileUser
from account.models import User
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
def upload_view(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    metadata_dict = request.META
    # print(metadata_dict)
    upload_file = request.body
    user_id = request.user_id
    # user_id = 2
    file_size = metadata_dict.get('HTTP_SIZE')
    file_hash = metadata_dict.get('HTTP_HASH')
    file_check_hash = metadata_dict.get('HTTP_CHECKHASH')
    file_id = metadata_dict.get('HTTP_FID')
    if file_size is None or file_hash is None or file_check_hash is None or file_id is None:
        return MyResponse.ERROR("参数错误1")
    # 检查空间是否足够
    usedSize = getUsedStorage(user_id)
    totalSize = gettotalSize(user_id)
    if usedSize + int(file_size) > totalSize:
        return MyResponse.ERROR("空间不足")
    # 检查文件上传起始点
    file_model = get_file_from_model(file_hash, file_check_hash, file_size)
    user_file = FileUser.objects.filter(id=file_id, user_id=user_id, is_delete=False)
    if len(user_file) == 0:
        return MyResponse.ERROR("fid错误")
    user_file = user_file[0]
    if upload_file is None or len(upload_file) == 0:
        file_model.broken = not check_file(file_hash)
        file_model.save()
        if not file_model.broken:
            user_file.file = file_model
            user_file.is_uploaded = True
            user_file.save()
            return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "文件已保存", "next": False})
        return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "查询成功", "next": True})
    # 上传文件
    start_byte = int(metadata_dict.get('HTTP_STARTBYTE'))
    chunk_hash = metadata_dict.get('HTTP_CHUNKHASH')
    if start_byte is None or not chunk_hash:
        return MyResponse.ERROR("参数错误2")
    file_path = (settings.STATIC_FILES_DIR_FILE / file_hash).absolute()  # 更改文件保存路径
    mode = 'wb' if start_byte == 0 else 'ab'  # 如果文件不存在则创建新文件，存在则以追加模式续写
    if chunk_hash != get_file_hash_file(upload_file):
        return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "文件损坏", "next": True})
    with open(file_path, mode) as destination:
        if upload_file:
            # 移动文件指针到指定位置开始写入
            destination.seek(start_byte)
            destination.write(upload_file)
    size = os.path.getsize(file_path)
    file_model.upload_size = size
    file_model.broken=not check_file(file_hash)
    file_model.save()
    # 检查文件是否存在
    if not file_model.broken:
        user_file.file = file_model
        user_file.is_uploaded = True
        user_file.save()
        return MyResponse.SUCCESS({"upload_size": file_model.upload_size,"message": "文件已保存",  "next": False})
    return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "上传成功,准备下一块", "next": True})
