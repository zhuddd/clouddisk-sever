import asyncio
import os
import re

from asgiref.sync import sync_to_async
from django.http import  StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from sever import settings
from utils.LoginCheck import LoginCheck, AsyncLoginCheck
from utils.MyResponse import MyResponse
from utils.file import get_user_file_by_id, get_user_tree_by_id


@AsyncLoginCheck
async def download(request):
    if request.method != "GET":
        return MyResponse.ERROR("请求方式错误")
    user_id = request.user_id
    # user_id = 2
    file_id = request.GET.get("file_id")
    if not file_id:
        return MyResponse.ERROR("参数错误")
    # 获取文件信息
    file_user = await sync_to_async(get_user_file_by_id)(user_id, file_id)
    if file_user is None:
        return MyResponse.ERROR("文件不存在 code:A")
    file = await sync_to_async(lambda: file_user.file)()
    if file is None:
        return MyResponse.ERROR("文件不存在 code:B")
    only_header = request.GET.get("Only_header")
    file_path = settings.STATIC_FILES_DIR_FILE / file.hash
    file_name = file_user.file_name
    if not file_path.exists():
        return MyResponse.ERROR("文件已失效")
    if only_header == "True":
        file_info = {
            "file_name": file_user.file_name,
            "file_size": file.size,
            "file_hash": file.hash,
        }
        return MyResponse.SUCCESS(file_info)
    else:
        start_bytes = re.search(r'bytes=(\d+)-', request.META.get('HTTP_RANGE', ''), re.S)
        start_bytes = int(start_bytes.group(1)) if start_bytes else 0

        async def file_iterator(file_path, chunk_size=1024 * 1024 * 10):
            with open(file_path, 'rb') as f:
                f.seek(start_bytes, os.SEEK_SET)
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
                    await asyncio.sleep(0.1)

        response = StreamingHttpResponse(file_iterator(file_path), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename={escape_uri_path(file_name)}'
        response['Content-Length'] = file.size - start_bytes
        response['Hash'] = file.hash
        response.status_code = 200 if start_bytes == 0 else 206
        return response


@LoginCheck
def get_tree(request):
    if request.method != "POST":
        return MyResponse.ERROR("请求方式错误")
    user_id = request.user_id
    # user_id = 2
    file_id = request.POST.get("file_id")
    if not file_id:
        return MyResponse.ERROR("参数错误")
    # 获取文件信息
    tree = get_user_tree_by_id(user_id, file_id)
    if tree is None:
        return MyResponse.ERROR("文件不存在")
    return MyResponse.SUCCESS(tree)
