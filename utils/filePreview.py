import mimetypes
import os
import re

from asgiref.sync import sync_to_async
from django.http import StreamingHttpResponse, FileResponse, HttpRequest
from django.shortcuts import render

from sever import settings
from utils.account import get_user_by_session
from utils.file import get_user_file_by_id


async def file_iterator(path, offset, length):
    """文件流迭代器"""
    with open(path, 'rb') as f:
        f.seek(offset)
        while length > 0:
            data = f.read(1024 * 1024)
            if not data:
                break
            length -= len(data)
            yield data


async def file_iterator_all(file_path, chunk_size=1024 * 1024 * 10):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


async def fileInfo(user_id, file_id):
    """获取文件信息"""
    file_user = await sync_to_async(get_user_file_by_id)(user_id, file_id)
    if file_user is None:
        return None, None
    file = await sync_to_async(lambda: file_user.file)()
    if file is None:
        return None, None
    file_name = await sync_to_async(lambda: file_user.file_name)()
    file_hash = await sync_to_async(lambda: file.hash)()
    return file_name, file_hash


async def preview_box(request: HttpRequest, user, file_id, k):
    name, file_hash = await fileInfo(user, file_id)
    if name is None or file_hash is None:
        return render(request, 'previewError.html')
    content_type, _ = mimetypes.guess_type(name)
    if content_type is None:
        return render(request, 'previewError.html')
    type = content_type.split("/")[0]

    if type in ("video", "audio"):
        return render(request,
                      f'{type}.html',
                      {
                          "url": f"./../data/{k}",
                          "type": content_type,
                          "name": name,
                          "poster": f"./../poster/{k}"}
                      )
    else:
        return render(request, 'previewError.html')


async def all_preview(request, user_id, file_id):
    """以流媒体的方式响应视频文件"""
    name, file_hash = await fileInfo(user_id, file_id)
    path = settings.STATIC_FILES_DIR_FILE / file_hash
    content_type, encoding = mimetypes.guess_type(name)
    if content_type is None:
        return render(request, 'previewError.html')

    # 处理请求中的范围头信息
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)

    if range_match:
        # 处理分片请求
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 10
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1

        # 构建分片响应
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        # 处理完整文件请求
        resp = FileResponse(open(path, "rb"), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp



