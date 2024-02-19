from functools import wraps

from asgiref.sync import sync_to_async

from utils.MyResponse import MyResponse
from utils.account import get_user_by_session


def LoginCheck(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        session = request.COOKIES.get("session", "")
        user_id = get_user_by_session(session)
        if user_id is None:
            print(request.COOKIES)
            print("LoginCheck:",request.path)
            return MyResponse.ERROR("请先登录")
        else:
            request.user_id = user_id
            return view_func(request, *args, **kwargs)

    return wrapped_view

def AsyncLoginCheck(view_func):
    @wraps(view_func)
    async def wrapped_view(request, *args, **kwargs):
        session = request.COOKIES.get("session", "")
        user_id = await sync_to_async(get_user_by_session)(session)
        if user_id is None:
            print(request.COOKIES)
            print("LoginCheck:",request.path)
            return MyResponse.ERROR("请先登录")
        else:
            request.user_id = user_id
            return await view_func(request, *args, **kwargs)

    return wrapped_view