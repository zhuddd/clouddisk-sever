# Create your views here.
import json
import os

from django.http import JsonResponse

from utils.CommonLog import log
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
    except Exception as e:
        log.warning(f"创建上传文件夹失败:{e}，userid:{user_id}，{request.POST}")
        return MyResponse.ERROR("参数错误2")


def validate_request_params(metadata_dict):
    required_keys = ['HTTP_SIZE', 'HTTP_HASH', 'HTTP_CHECKHASH', 'HTTP_FID']
    for key in required_keys:
        if metadata_dict.get(key) is None:
            return False
    return True

def check_user_space(user_id, file_size):
    used_size = getUsedStorage(user_id)
    total_size = gettotalSize(user_id)
    return used_size + file_size <= total_size

def handle_file_upload(upload_file, file_model, user_file, metadata_dict):
    start_byte = int(metadata_dict.get('HTTP_STARTBYTE', 0))
    chunk_hash = metadata_dict.get('HTTP_CHUNKHASH')
    file_path = (settings.STATIC_FILES_DIR_FILE / file_model.hash).absolute()
    mode = 'wb' if start_byte == 0 else 'ab'

    # Check chunk hash
    if chunk_hash != get_file_hash_file(upload_file):
        return MyResponse.ERROR("文件损坏")

    # Write file chunk
    with open(file_path, mode) as destination:
        destination.seek(start_byte)
        destination.write(upload_file)

    # Update file model and user file
    file_model.upload_size = os.path.getsize(file_path)
    file_model.save()
    if file_model.upload_size == file_model.size:
        file_model.broken = not check_file(file_model.hash)
        file_model.save()
        if not file_model.broken:
            user_file.file = file_model
            user_file.is_uploaded = True
            user_file.save()
            return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "文件已保存", "next": False})
        else:
            return MyResponse.SUCCESS({"upload_size": 0, "message": "文件损坏，请重新上传", "next": True})

    return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "上传成功，准备下一块", "next": True})

@LoginCheck
def upload_view(request):
    try:
        if request.method != "POST":
            return MyResponse.ERROR("请求方式错误")

        metadata_dict = request.META
        upload_file = request.body
        user_id = request.user_id
        file_size = int(metadata_dict.get('HTTP_SIZE', 0))
        file_hash = metadata_dict.get('HTTP_HASH')
        file_check_hash = metadata_dict.get('HTTP_CHECKHASH')
        file_id = metadata_dict.get('HTTP_FID')

        if not validate_request_params(metadata_dict):
            return MyResponse.ERROR("参数错误")

        if not check_user_space(user_id, file_size):
            return MyResponse.ERROR("空间不足")

        file_model = get_file_from_model(file_hash, file_check_hash, file_size)
        user_file = FileUser.objects.filter(id=file_id, user_id=user_id, is_delete=False).first()

        if not user_file:
            return MyResponse.ERROR("fid错误")

        if not upload_file:
            if not file_model.broken:
                user_file.file = file_model
                user_file.is_uploaded = True
                user_file.save()
                return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "文件已保存", "next": False})
            else:
                if file_model.upload_size == file_model.size:
                    file_model.broken = not check_file(file_hash)
                    file_model.save()
                    if not file_model.broken:
                        user_file.file = file_model
                        user_file.is_uploaded = True
                        user_file.save()
                        return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "文件已保存", "next": False})
                    else:
                        return MyResponse.SUCCESS({"upload_size": 0, "message": "文件损坏，请重新上传", "next": True})
                else:
                    return MyResponse.SUCCESS({"upload_size": file_model.upload_size, "message": "查找成功", "next": True})
        else:
            return handle_file_upload(upload_file, file_model, user_file, metadata_dict)

    except Exception as e:
        log.warning(f"上传文件失败: {e}，userid: {request.user_id}，{request.POST}")
        return MyResponse.ERROR("上传失败")

